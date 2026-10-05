import streamlit as st
from db.database import init_db, get_student


def topic_names(student):
    out = []
    for t in student.get("topics") or []:
        out.append(t["name"] if isinstance(t, dict) and "name" in t else str(t))
    return out


def sidebar_login():
    init_db()
    sid = st.session_state.get("student_id")
    if not sid:
        return None
    s = get_student(sid)
    if not s:
        st.session_state.pop("student_id", None)
        return None
    st.session_state["language"] = s["language"]
    st.session_state["hours"] = s["study_hours_per_day"]
    st.sidebar.write(f"👤 Logged in as **{s['name']}**")
    if st.sidebar.button("Log out"):
        for k in ("student_id", "quiz", "wquiz"):
            st.session_state.pop(k, None)
        st.rerun()
    return sid


def require_student():
    sid = sidebar_login()
    if not sid:
        st.warning("Please log in on the Home page first.")
        st.stop()
    return sid, get_student(sid)