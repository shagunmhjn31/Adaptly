import streamlit as st
from db.database import save_profile, get_profile
from core.profile import QUESTIONS, TRAIT_LABELS, score, study_settings, tips
from core.session import require_student
from core.style import inject_css
from core.i18n import t, lang_rule
from core.llm import ask

inject_css()
sid, student = require_student()

lang = student["language"]
i = 1 if lang == "Hindi" else 0   # 0 = English text, 1 = Hinglish text

st.title(t("diag_title"))
st.caption(t("diag_caption"))

TIMES = ["Morning", "Afternoon", "Night"]
TIME_KEY = {"Morning": "morning", "Afternoon": "afternoon", "Night": "night"}

with st.form("personality"):
    picks = []
    for n, q in enumerate(QUESTIONS):
        picks.append(st.radio(f"{n + 1}. {q['q'][i]}", [0, 1, 2],
                              format_func=lambda k, q=q: q["options"][k][i],
                              index=None, key=f"q{n}"))
    best_time = st.radio(t("best_time_q"), TIMES, format_func=lambda x: t(TIME_KEY[x]), index=None)
    done = st.form_submit_button(t("submit"))

if done:
    if None in picks or best_time is None:
        st.error(t("answer_all"))
    else:
        pts = [q["options"][k][2] for q, k in zip(QUESTIONS, picks)]
        traits = score(pts)
        traits["best_time"] = best_time
        settings = study_settings(traits)
        tip_list = tips(traits, lang)
        summary = "\n\n".join(tip_list)
        try:
            with st.spinner(t("ai_summary_wait")):
                prompt = (f"A student's study-style scores (1=low, 3=high): {traits}. "
                          f"{lang_rule(lang)} "
                          "Write a short, warm, encouraging 3-4 line summary of their study style "
                          "and how to study best. Do NOT diagnose anything or label them negatively.")
                summary = ask(prompt) + "\n\n" + summary
        except Exception:
            pass  # rule-based tips still work
        save_profile(sid, {**traits, "settings": settings}, summary)
        st.success(t("saved"))

profile = get_profile(sid)
if profile:
    st.subheader(t("your_style"))
    tr = profile["traits"]
    cols = st.columns(5)
    for col, (key, labels) in zip(cols, TRAIT_LABELS.items()):
        col.metric(labels[i], f"{tr[key]} / 3")
    s = tr["settings"]
    st.info(t("info_line", best=t(TIME_KEY.get(tr["best_time"], "morning")),
              f=s["focus_min"], b=s["break_min"], buf=s["buffer_pct"]))
    st.write(profile["summary"])