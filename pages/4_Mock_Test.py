import time, random
import pandas as pd
import streamlit as st
from core.session import require_student, topic_names
from core.style import inject_css
from core.i18n import t
from core.mock_test import generate_mcqs
from core.diagnostic import evaluate, behavior_notes
from db.database import save_result, save_test_session, latest_topic_scores, set_weak_topics

inject_css()
sid, student = require_student()
st.title(t("mt_title"))
st.caption(t("mt_caption"))

topics = topic_names(student)
extra = st.text_input(t("mt_extra"))
topics += [x.strip() for x in extra.split(",") if x.strip()]
if not topics:
    st.warning(t("mt_none"))
    st.stop()

mode = st.radio(t("mt_type"), ["diag", "topic"], format_func=lambda k: t("mt_type_" + k), horizontal=True)
c1, c2 = st.columns(2)
n = c1.slider(t("mt_n"), 5, 20, 10)
difficulty = c2.select_slider(t("mt_diff"), ["Easy", "Medium", "Hard"], value="Medium",
                              format_func=lambda x: t("diff_" + x))
chosen = []
if mode == "topic":
    chosen = st.multiselect(t("mt_choose"), topics, default=topics[:3])

if st.button(t("mt_generate")):
    pool = chosen if mode == "topic" else random.sample(topics, min(n, len(topics)))
    if not pool:
        st.error(t("mt_choose_one"))
    else:
        try:
            with st.spinner(t("mt_writing")):
                qs = generate_mcqs(pool, n, student["language"], difficulty)
            st.session_state["quiz"] = {"id": int(time.time()), "qs": qs, "start": time.time(),
                                        "mode": mode, "result": None}
        except Exception as e:
            st.error(t("mt_error"))
            st.caption(str(e)[:200])

quiz = st.session_state.get("quiz")

if quiz and quiz["result"] is None:
    with st.form("quiz_form"):
        answers = []
        for i, q in enumerate(quiz["qs"]):
            answers.append(st.radio(f"{i + 1}. [{q['topic']}] {q['question']}", q["options"],
                                    index=None, key=f"ans{quiz['id']}_{i}"))
        submit = st.form_submit_button(t("mt_submit"))
    if submit:
        res = evaluate(quiz["qs"], answers, time.time() - quiz["start"])
        source = "diagnostic" if quiz["mode"] == "diag" else "mock"
        for tp, d in res["per_topic"].items():
            save_result(sid, tp, d["correct"], d["total"], source)
        save_test_session(sid, source, res["total"], res["correct"], res["avg_sec"],
                          res["skipped"], res["first_half"], res["second_half"])
        weak = [tp for tp, p in latest_topic_scores(sid).items() if p < 60]
        set_weak_topics(sid, weak)
        quiz["result"] = res
        st.rerun()

elif quiz and quiz["result"]:
    res = quiz["result"]
    st.subheader(t("score_line", c=res["correct"], n=res["total"]))
    st.dataframe(pd.DataFrame([
        {t("col_topic"): tp, t("col_correct"): d["correct"], t("col_total"): d["total"],
         t("col_score"): round(d["correct"] / d["total"] * 100)}
        for tp, d in res["per_topic"].items()]), use_container_width=True)

    for note in behavior_notes(res, student["language"]):
        st.info(note)

    with st.expander(t("mt_expl")):
        for q, a in zip(quiz["qs"], res["answers"]):
            right = q["options"][q["answer"]]
            if a != right:
                st.markdown(f"**{q['question']}**  \n{t('mt_correct_ans')}: **{right}**  \n{q['explanation']}")

    weak = [tp for tp, p in latest_topic_scores(sid).items() if p < 60]
    if weak:
        st.warning(t("mt_weak") + ", ".join(weak))
        st.success(t("mt_weak_ok"))
    else:
        st.success(t("mt_noweak"))
    if st.button(t("mt_new")):
        st.session_state["quiz"] = None
        st.rerun()