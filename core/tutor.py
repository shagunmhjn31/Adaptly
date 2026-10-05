from datetime import date
from db.database import get_student, get_goals
from core.planner import plan_for
from core.i18n import lang_rule


def build_context(sid):
    s = get_student(sid)
    plan = plan_for(sid)
    today = [r for r in plan["schedule"] if r["date"] == date.today()]
    goals = get_goals(sid)
    lines = [f"Student name: {s['name']}",
             f"Preferred language: {s['language']}",
             "Reply rule: " + lang_rule(s["language"])]
    if goals:
        lines.append("Goals: " + "; ".join(
            f"{g['name']} (deadline {g['deadline']}, {g['covered']}% done)" for g in goals))
    if plan["weak"]:
        lines.append("Weak topics: " + ", ".join(plan["weak"]))
    if today:
        lines.append("Today's plan: " + "; ".join(
            f"{r['goal']} - {r['topic']} ({r['minutes']} min)" for r in today))
    return "\n".join(lines)


def system_helper(ctx):
    return f"""You are Adaptly, a friendly study helper for a school/college student.
Student context:
{ctx}

Rules:
- Follow the "Reply rule" in the student context for the language and script.
- Keep answers short and clear, with a small example when useful.
- If asked for practice questions, give the questions first and the answers only after the student tries.
- Prefer helping with the student's weak topics and today's plan when relevant.
- If you are not sure about something, say so and suggest checking the textbook or a teacher.
- Never diagnose stress or anxiety. If the student seems very distressed, be kind and suggest talking to a teacher, parent or counselor."""


def system_teachback(ctx, topic):
    return f"""You are a curious beginner classmate. The student will explain the topic "{topic}" to you.
Student context:
{ctx}

Rules:
- Follow the "Reply rule" in the student context for the language and script.
- Do NOT explain the topic yourself. React like a beginner: ask 1-2 simple follow-up questions per turn.
- Gently point out gaps, missing steps or misconceptions you notice.
- When the student asks for feedback, give: (1) what was correct, (2) what was missing or wrong, (3) a score out of 10, (4) one thing to revise.
- Be encouraging, never harsh."""