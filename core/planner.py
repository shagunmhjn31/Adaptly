import json
from datetime import date, timedelta

DEFAULT_SETTINGS = {"focus_min": 40, "break_min": 10, "buffer_pct": 10}


def split_time(goals, hours_per_day, today=None):
    """weight = marks x syllabus left x difficulty / sqrt(days left)"""
    today = today or date.today()
    rows = []
    for g in goals:
        days_left = (date.fromisoformat(g["deadline"]) - today).days
        if days_left < 0:
            continue
        days_left = max(days_left, 1)
        remaining = (100 - g["covered"]) / 100
        need = g["marks"] * remaining * g["difficulty"]
        weight = need / (days_left ** 0.5)
        rows.append({"id": g.get("id"), "name": g["name"], "kind": g["kind"],
                     "days_left": days_left, "weight": weight})
    total = sum(r["weight"] for r in rows) or 1
    for r in rows:
        share = r["weight"] / total
        r["share_pct"] = round(share * 100, 1)
        r["hours_per_day"] = round(share * hours_per_day, 2)
        r["total_hours"] = round(r["hours_per_day"] * r["days_left"], 1)
    return rows


def _topic_list(g):
    try:
        return json.loads(g.get("topics") or "[]")
    except Exception:
        return []


def build_schedule(goals, hours_per_day, settings=None, weak=None, load_factor=1.0,
                   today=None, max_days=45):
    settings = settings or DEFAULT_SETTINGS
    weak = set(weak or [])
    today = today or date.today()
    active = [g for g in goals if date.fromisoformat(g["deadline"]) >= today]
    if not active:
        return []
    exam_dates = [date.fromisoformat(g["deadline"]) for g in active if g["kind"] == "Exam"]
    end = min(max(date.fromisoformat(g["deadline"]) for g in active), today + timedelta(days=max_days))

    counters, schedule = {}, []
    day = today
    while day <= end:
        hrs = hours_per_day * (1 - settings["buffer_pct"] / 100) * load_factor
        exam_week = any(0 <= (d - day).days <= 7 for d in exam_dates)
        if exam_week:
            hrs *= 0.85  # lighter, revision-focused final week

        for r in split_time(active, hrs, today=day):
            g = next(x for x in active if x["id"] == r["id"])
            topics = _topic_list(g)
            total_days = max((date.fromisoformat(g["deadline"]) - today).days, 1)
            revision = r["days_left"] <= max(2, int(0.25 * total_days))
            phase = "Revision" if revision else "Learn"

            if topics:
                if revision:
                    cycle = [t for t in topics if t in weak] + [t for t in topics if t not in weak]
                else:
                    pending = topics[int(len(topics) * g["covered"] / 100):] or topics
                    cycle = pending + [t for t in pending if t in weak]  # weak topics come twice
                key = (g["id"], phase)
                i = counters.get(key, 0)
                counters[key] = i + 1
                topic = cycle[i % len(cycle)]
            else:
                topic = "General study"

            minutes = round(r["hours_per_day"] * 60)
            if minutes < 5:
                continue
            schedule.append({
                "date": day, "goal": g["name"], "topic": topic, "phase": phase,
                "minutes": minutes,
                "sessions": max(1, round(minutes / settings["focus_min"])),
                "note": "exam_week" if exam_week else "",
            })
        day += timedelta(days=1)
    return schedule


def plan_for(sid, hours=None):
    """Everything in one call: reads DB, builds the live schedule."""
    from db.database import get_student, get_goals, get_profile, latest_topic_scores, missed_topics
    from core.wellbeing import load_factor

    student = get_student(sid)
    goals = get_goals(sid)
    profile = get_profile(sid)
    settings = profile["traits"]["settings"] if profile else DEFAULT_SETTINGS
    hours = hours or student["study_hours_per_day"] or 4.0

    weak = {t for t, p in latest_topic_scores(sid).items() if p < 60} | set(missed_topics(sid))
    factor, stressed = load_factor(sid)
    sched = build_schedule(goals, hours, settings, weak, factor)
    return {"schedule": sched, "settings": settings, "weak": sorted(weak),
            "stressed": stressed, "factor": factor}