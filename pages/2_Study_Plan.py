import json
import pandas as pd
import streamlit as st
from datetime import date, timedelta
from db.database import (add_goal, get_goals, delete_goal, update_goal_progress,
                         log_study, get_study_log)
from core.planner import split_time, plan_for
from core.session import require_student, topic_names
from core.style import inject_css
from core.i18n import t, lang_rule
from core.llm import ask

inject_css()
sid, student = require_student()
st.title(t("sp_title"))


def show_topic(x):
    return t("general") if x == "General study" else x


with st.expander(t("sp_new"), expanded=not get_goals(sid)):
    with st.form("goal", clear_on_submit=True):
        name = st.text_input(t("sp_name"))
        kind = st.selectbox(t("sp_type"), ["Exam", "Self-study"], format_func=lambda k: t("type_" + k))
        deadline = st.date_input(t("sp_deadline"), value=date.today() + timedelta(days=14))
        marks = st.number_input(t("sp_marks"), 1.0, 1000.0, 100.0)
        difficulty = st.slider(t("sp_diff"), 1, 5, 3)
        covered = st.slider(t("sp_covered"), 0, 100, 0)
        use_syl = st.checkbox(t("sp_use_syl"))
        topics_text = st.text_area(t("sp_topics_text"))
        weaknesses = st.text_area(t("sp_weak"))
        ok = st.form_submit_button(t("sp_add"))
    if ok:
        if not name:
            st.error(t("sp_name_err"))
        else:
            topics = topic_names(student) if use_syl else []
            topics += [x.strip() for x in topics_text.splitlines() if x.strip()]
            add_goal(sid, name, kind, deadline, marks, difficulty, covered, weaknesses, topics)
            st.rerun()

goals = get_goals(sid)
if not goals:
    st.info(t("sp_none"))
    st.stop()

st.header(t("sp_tasks"))
for g in goals:
    c1, c2 = st.columns([6, 1])
    n_topics = len(json.loads(g.get("topics") or "[]"))
    c1.write(t("sp_task_line", name=g["name"], kind=t("type_" + g["kind"]), deadline=g["deadline"],
               marks=g["marks"], diff=g["difficulty"], cov=g["covered"], n=n_topics))
    if c2.button(t("sp_delete"), key=f"del{g['id']}"):
        delete_goal(g["id"])
        st.rerun()

with st.expander(t("sp_progress")):
    with st.form("progress"):
        new_vals = {g["id"]: st.slider(g["name"], 0, 100, int(g["covered"]), key=f"cov{g['id']}") for g in goals}
        if st.form_submit_button(t("sp_save_progress")):
            for gid, v in new_vals.items():
                update_goal_progress(gid, v)
            st.rerun()

st.header(t("sp_plan"))
hours = st.number_input(t("sp_hours"), 1.0, 16.0, float(student["study_hours_per_day"] or 4.0), 0.5)
plan = plan_for(sid, hours)
sched = plan["schedule"]

if plan["stressed"]:
    st.warning(t("sp_stressed"))
exam_dates = [date.fromisoformat(g["deadline"]) for g in goals if g["kind"] == "Exam"]
if any(0 <= (d - date.today()).days <= 7 for d in exam_dates):
    st.info(t("sp_examweek"))
if plan["weak"]:
    st.caption(t("sp_priority") + ", ".join(plan["weak"]))

log = get_study_log(sid)
yesterday = (date.today() - timedelta(days=1)).isoformat()
if any(r["day"] == yesterday and r["planned"] > 0 and r["done"] == 0 for r in log):
    st.info(t("sp_missed"))

s = plan["settings"]
today_rows = [r for r in sched if r["date"] == date.today()]
st.subheader(t("sp_today"))
if not today_rows:
    st.write(t("sp_no_today"))
else:
    prev = {(r["day"], r["goal_name"]): r["done"] for r in log}
    with st.form("today"):
        checks = []
        for i, r in enumerate(today_rows):
            was_done = prev.get((date.today().isoformat(), r["goal"]), 0) > 0
            checks.append(st.checkbox(
                t("sp_today_line", goal=r["goal"], topic=show_topic(r["topic"]),
                  phase=t("phase_" + r["phase"]), m=r["minutes"], s=r["sessions"],
                  f=s["focus_min"], b=s["break_min"]),
                value=was_done, key=f"chk{i}"))
        if st.form_submit_button(t("sp_save_today")):
            for r, c in zip(today_rows, checks):
                log_study(sid, date.today(), r["goal"], r["topic"], r["minutes"], r["minutes"] if c else 0)
            st.success(t("sp_saved"))
            st.rerun()
    if today_rows[0]["note"]:
        st.caption(t("note_" + today_rows[0]["note"]))

with st.expander(t("sp_14")):
    upto = date.today() + timedelta(days=14)
    df = pd.DataFrame([{
        t("col_date"): r["date"].strftime("%a %d %b"), t("col_goal"): r["goal"],
        t("col_topic"): show_topic(r["topic"]), t("col_phase"): t("phase_" + r["phase"]),
        t("col_min"): r["minutes"], t("col_sessions"): r["sessions"],
        t("col_note"): t("note_" + r["note"]) if r["note"] else ""}
        for r in sched if r["date"] <= upto])
    if not df.empty:
        st.dataframe(df, use_container_width=True)

st.subheader(t("sp_share"))
rows = split_time(goals, hours)
if rows:
    df2 = pd.DataFrame([{
        t("col_goal"): r["name"], t("col_type"): t("type_" + r["kind"]),
        t("col_days_left"): r["days_left"], t("col_share"): r["share_pct"],
        t("col_hours"): r["hours_per_day"]} for r in rows])
    st.dataframe(df2, use_container_width=True)
    st.bar_chart(df2.set_index(t("col_goal"))[t("col_hours")])

st.header(t("sp_advice_h"))
if st.button(t("sp_advice_btn")):
    for g in goals:
        if (g["weaknesses"] or "").strip():
            try:
                with st.spinner(f"{g['name']}..."):
                    tip = ask(f"Student's goal: {g['name']} ({g['kind']}). Weaknesses: {g['weaknesses']}. "
                              f"Give 4 short, practical study tips. {lang_rule(student['language'])}")
                st.subheader(g["name"])
                st.write(tip)
            except Exception:
                st.warning(t("sp_busy", name=g["name"]))