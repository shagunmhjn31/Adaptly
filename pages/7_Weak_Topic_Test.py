import time
import pandas as pd
import streamlit as st
from core.session import require_student, topic_names
from core.style import inject_css
from core.i18n import t, lang_rule
from core.weak_test import weak_topic_list, level_for, generate_weak_test
from core.diagnostic import evaluate, behavior_notes
from core.llm import ask
from db.database import save_result, save_test_session, latest_topic_scores, set_weak_topics

inject_css()
sid, student = require_student()
st.title(t("wt_title"))
st.caption(t("wt_caption"))

weak, scores = weak_topic_list(sid)

if weak:
    st.subheader(t("wt_weak_h"))
    st.dataframe(pd.DataFrame([
        {t("col_topic"): tp, t("wt_cur"): scores.get(tp, t("wt_new")),
         t("wt_level"): t("diff_" + level_for(scores.get(tp)))} for tp in weak]),
        use_container_width=True)
else:
    st.info(t("wt_none"))

options = sorted(set(topic_names(student)) | set(weak))
chosen = st.multiselect(t("wt_topics"), options, default=weak[:5])
c1, c2 = st.columns(2)
n = c1.slider(t("wt_n"), 5, 20, 10)
aptitude = c2.checkbox(t("wt_apt"))

if st.button(t("wt_generate")):
    if not chosen:
        st.error(t("mt_choose_one"))
    else:
        try:
            with st.spinner(t("wt_writing")):
                qs = generate_weak_test(chosen, scores, n, student["language"], aptitude)
            st.session_state["wquiz"] = {"id": int(time.time()), "qs": qs, "start": time.time(),
                                         "before": dict(scores), "result": None}
        except Exception as e:
            st.error(t("wt_error"))
            st.caption(str(e)[:200])

quiz = st.session_state.get("wquiz")

if quiz and quiz["result"] is None:
    with st.form("wquiz_form"):
        answers = []
        for i, q in enumerate(quiz["qs"]):
            answers.append(st.radio(f"{i + 1}. [{q['topic']}] {q['question']}", q["options"],
                                    index=None, key=f"w{quiz['id']}_{i}"))
        submit = st.form_submit_button(t("mt_submit"))
    if submit:
        res = evaluate(quiz["qs"], answers, time.time() - quiz["start"])
        for tp, d in res["per_topic"].items():
            save_result(sid, tp, d["correct"], d["total"], "weak_test")
        save_test_session(sid, "weak_test", res["total"], res["correct"], res["avg_sec"],
                          res["skipped"], res["first_half"], res["second_half"])
        set_weak_topics(sid, [tp for tp, p in latest_topic_scores(sid).items() if p < 60])
        quiz["result"] = res
        st.rerun()

elif quiz and quiz["result"]:
    res, before = quiz["result"], quiz["before"]
    after = latest_topic_scores(sid)
    st.subheader(t("score_line", c=res["correct"], n=res["total"]))

    rows, improved = [], []
    for tp, d in res["per_topic"].items():
        now = round(d["correct"] / d["total"] * 100)
        old = before.get(tp)
        key = "tr_new" if old is None else ("tr_up" if now > old else ("tr_same" if now == old else "tr_down"))
        if key == "tr_up":
            improved.append(tp)
        rows.append({t("col_topic"): tp, t("wt_before"): old if old is not None else "-",
                     t("wt_now"): now, t("wt_trend"): t(key)})
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    for note in behavior_notes(res, student["language"]):
        st.info(note)

    if improved:
        st.success(t("wt_improved") + ", ".join(improved) + " 🎉")

    still_weak = [tp for tp in res["per_topic"] if after.get(tp, 0) < 60]
    if still_weak:
        st.warning(t("wt_still") + ", ".join(still_weak) + t("wt_still2"))
        if st.button(t("wt_notes_btn")):
            try:
                with st.spinner(t("wt_notes_wait")):
                    notes = ask(t("wt_notes_prompt", topics=", ".join(still_weak)).replace(
                        "{topics}", ", ".join(still_weak)) + " " + lang_rule(student["language"]),
                        max_tokens=3000)
                st.markdown(notes)
                st.caption(t("wt_verify"))
            except Exception:
                st.warning(t("wt_busy"))
    else:
        st.success(t("wt_all_ok"))

    with st.expander(t("mt_expl")):
        for q, a in zip(quiz["qs"], res["answers"]):
            right = q["options"][q["answer"]]
            if a != right:
                st.markdown(f"**{q['question']}**  \n{t('mt_correct_ans')}: **{right}**  \n{q['explanation']}")

    if st.button(t("wt_new_btn")):
        st.session_state["wquiz"] = None
        st.rerun()