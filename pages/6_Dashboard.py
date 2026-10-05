import pandas as pd
import streamlit as st
from datetime import date, timedelta
from core.session import require_student
from core.style import inject_css
from core.i18n import t
from db.database import get_test_sessions, get_study_log, latest_topic_scores, get_checkins

inject_css()
sid, student = require_student()
st.title(t("db_title"))

sessions = get_test_sessions(sid)
log = get_study_log(sid)
scores = latest_topic_scores(sid)

done_days = {r["day"] for r in log if r["done"] > 0}
d = date.today()
if d.isoformat() not in done_days:
    d -= timedelta(days=1)
streak = 0
while d.isoformat() in done_days:
    streak += 1
    d -= timedelta(days=1)

planned = sum(r["planned"] for r in log)
done = sum(r["done"] for r in log)
total_q = sum(s["n"] for s in sessions)
total_c = sum(s["correct"] for s in sessions)

c1, c2, c3, c4 = st.columns(4)
c1.metric(t("db_streak"), t("db_days", n=streak))
c2.metric(t("db_total"), f"{round(done / 60, 1)} hrs")
c3.metric(t("db_follow"), f"{round(done / planned * 100) if planned else 0}%")
c4.metric(t("db_tests"), f"{len(sessions)} ({round(total_c / total_q * 100) if total_q else 0}% avg)")

if sessions:
    st.subheader(t("db_scores"))
    df = pd.DataFrame(sessions)
    df["score"] = (df["correct"] / df["n"] * 100).round()
    st.line_chart(df.set_index("ts")["score"])

if scores:
    st.subheader(t("db_strength"))
    st.bar_chart(pd.Series(scores).sort_values().rename("score"))
    weak = [tp for tp, p in scores.items() if p < 60]
    if weak:
        st.warning(t("db_weak") + ", ".join(weak))

if log:
    st.subheader(t("db_daily"))
    st.bar_chart(pd.DataFrame(log).groupby("day")["done"].sum())

moods = get_checkins(sid, 14)
if moods:
    st.subheader(t("db_mood"))
    st.line_chart(pd.DataFrame(moods).sort_values("day").set_index("day")["mood"])

if not (sessions or log or moods):
    st.info(t("db_nodata"))