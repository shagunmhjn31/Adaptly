import streamlit as st
from core.session import require_student, topic_names
from core.style import inject_css
from core.i18n import t
from core.tutor import build_context, system_helper, system_teachback
from core.llm import chat_stream

inject_css()
sid, student = require_student()

st.title(t("helper_title"))
st.caption(t("helper_caption"))

mode = st.radio(t("mode"), ["doubt", "teach"], format_func=lambda k: t("mode_" + k), horizontal=True)
teach = mode == "teach"

topic = None
if teach:
    names = topic_names(student)
    topic = st.selectbox(t("pick_topic"), names) if names else st.text_input(t("topic_name"))
    if not topic:
        st.stop()
    st.info(t("teach_info"))

key = f"chat_{sid}_{'tb_' + topic if teach else 'doubt'}"
history = st.session_state.setdefault(key, [])

prompt = None
b1, b2 = st.columns(2)
if teach:
    if b1.button(t("btn_feedback")):
        prompt = t("feedback_prompt")
else:
    if b1.button(t("btn_practice")):
        prompt = t("practice_prompt")
if b2.button(t("btn_clear")):
    st.session_state[key] = []
    st.rerun()

for m in history:
    with st.chat_message(m["role"]):
        st.write(m["content"])

typed = st.chat_input(t("chat_input"))
prompt = typed or prompt

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    try:
        ctx = build_context(sid)
        system = system_teachback(ctx, topic) if teach else system_helper(ctx)
        with st.chat_message("assistant"):
            reply = st.write_stream(
                chat_stream(history + [{"role": "user", "content": prompt}], system))
        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(t("ai_error"))
        st.exception(e)