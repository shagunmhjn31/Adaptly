import streamlit as st
from db.database import (init_db, save_student, get_student, set_credentials,
                         username_taken, get_credentials)
from core.syllabus import read_pdf, extract_topics
from core.session import sidebar_login, topic_names
from core.style import inject_css
from core.auth import hash_password, verify_password
from core.i18n import t

st.set_page_config(page_title="Adaptly", page_icon="🎯", layout="wide")
inject_css()
init_db()
sid = sidebar_login()

st.markdown(
    f'<div class="hero"><h1>🎯 Adaptly</h1><p>{t("tagline")}</p></div>',
    unsafe_allow_html=True)

st.markdown("""
<style>
a[data-testid="stPageLink-NavLink"] { justify-content:center; width:100%; margin:-6px 0 18px; }
</style>""", unsafe_allow_html=True)

flash = st.session_state.pop("flash", None)
if flash:
    st.success(flash)

# icon, (English, Hinglish) title, (English, Hinglish) text, page, color
CARDS = [
    ("🧠", ("Study Style Check", "Study Style Check"),
     ("10 everyday questions find how you focus and plan. Your schedule is built around it.",
      "10 daily-life sawal se pata chalta hai aap kaise focus aur plan karte hain."),
     "pages/1_Diagnostic.py", "#7C74FF"),
    ("📝", ("Mock Tests", "Mock Tests"),
     ("Questions made from your own syllabus. Weak topics are found automatically.",
      "Aapke apne syllabus se sawal. Weak topics apne aap mil jate hain."),
     "pages/4_Mock_Test.py", "#22D3EE"),
    ("🎯", ("Weak-Topic Test", "Weak-Topic Test"),
     ("Practice only what you struggle with. Difficulty adapts to your score.",
      "Sirf wahi practice jo mushkil lagta hai. Difficulty score ke hisaab se badalti hai."),
     "pages/7_Weak_Topic_Test.py", "#F472B6"),
    ("📅", ("Smart Study Plan", "Smart Study Plan"),
     ("Time is split across exams by marks, difficulty and days left. Re-plans if you miss a day.",
      "Marks, difficulty aur bache din ke hisaab se time baatta hai. Din miss ho to plan badal jata hai."),
     "pages/2_Study_Plan.py", "#FBBF24"),
    ("🤖", ("AI Helper", "AI Sahayak"),
     ("Ask doubts, get practice questions, or teach the AI to find gaps in your understanding.",
      "Doubts poochhein, practice sawal lein, ya AI ko samjha kar apni kamiyan dhundhein."),
     "pages/3_AI_Helper.py", "#34D399"),
    ("💚", ("Wellbeing Check-in", "Wellbeing Check-in"),
     ("A 30-second check-in keeps your plan light when you are tired or stressed.",
      "30 second ka check-in. Thake ya stressed hone par plan halka ho jata hai."),
     "pages/5_Check_in.py", "#FB7185"),
    ("📊", ("Progress Dashboard", "Progress Dashboard"),
     ("See your streak, test scores, topic strengths and mood trend in one place.",
      "Streak, test scores, topic strength aur mood trend ek jagah dekhein."),
     "pages/6_Dashboard.py", "#60A5FA"),
]


def card_html(card, i):
    ico, title, text, _, color = card
    return (f'<div class="feat" style="--c:{color}"><div class="ico">{ico}</div>'
            f'<h4>{title[i]}</h4><p>{text[i]}</p></div>')


if sid:
    s = get_student(sid)
    i = 1 if s["language"] == "Hindi" else 0
    st.subheader(t("welcome", name=s["name"]))
    st.markdown(
        f'<span class="pill">🌐 {s["language"]}</span>'
        f'<span class="pill">⏱️ {s["study_hours_per_day"]} h / day</span>'
        f'<span class="pill">🎓 {s["exam_name"] or "-"}</span>',
        unsafe_allow_html=True)

    cols = st.columns(3, gap="medium")
    for n, card in enumerate(CARDS):
        with cols[n % 3]:
            st.markdown(card_html(card, i), unsafe_allow_html=True)
            st.page_link(card[3], label=("Open →" if i == 0 else "Kholein →"))

    names = topic_names(s)
    if names:
        with st.expander(t("syl_topics", n=len(names))):
            st.dataframe(s["topics"], use_container_width=True)
else:
    left, right = st.columns([1.1, 1], gap="large")

    with left:
        st.markdown("### Why Adaptly?")
        st.markdown('<div class="feat-grid">' + "".join(card_html(c, 0) for c in CARDS) + "</div>",
                    unsafe_allow_html=True)

    with right:
        tab_login, tab_signup = st.tabs(["🔑 Log in", "✨ Sign up"])

        with tab_login:
            with st.form("login"):
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                go = st.form_submit_button("Log in")
            if go:
                cred = get_credentials(u.strip())
                if cred and cred["pw_hash"] and verify_password(p, cred["pw_hash"], cred["salt"]):
                    st.session_state["student_id"] = cred["id"]
                    st.rerun()
                else:
                    st.error("Wrong username or password.")

        with tab_signup:
            with st.form("signup"):
                username = st.text_input("Choose a username")
                password = st.text_input("Choose a password (min 6 characters)", type="password")
                confirm = st.text_input("Confirm password", type="password")
                name = st.text_input("Your name")
                language = st.selectbox("Preferred language (Hindi = Hinglish)",
                                        ["English", "Hindi", "Punjabi"])
                exam_name = st.text_input("Main exam (e.g. Class 12 Board, Semester 3)")
                exam_date = st.date_input("Exam date")
                hours = st.slider("Hours you can study per day", 1.0, 12.0, 4.0, 0.5)
                uploaded = st.file_uploader("Upload syllabus (PDF)", type=["pdf"])
                pasted = st.text_area("...or paste your syllabus here")
                create = st.form_submit_button("Create account")

            if create:
                username = username.strip()
                if len(username) < 3 or len(password) < 6:
                    st.error("Username needs 3+ characters and password 6+ characters.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                elif username_taken(username):
                    st.error("That username is taken. Try another.")
                elif not name or not (uploaded or pasted):
                    st.error("Please add your name and a syllabus.")
                else:
                    try:
                        with st.spinner("Reading your syllabus..."):
                            text = read_pdf(uploaded) if uploaded else pasted
                            topics = extract_topics(text)
                            new_id = save_student(name, language, exam_name, exam_date, topics, hours)
                            h, salt = hash_password(password)
                            set_credentials(new_id, username, h, salt)
                        st.session_state["student_id"] = new_id
                        st.session_state["language"] = language
                        st.session_state["flash"] = t("acct_created", n=len(topics))
                        st.rerun()
                    except Exception as e:
                        st.error("Could not read the syllabus. Please try again in a moment.")
                        st.caption(str(e)[:200])