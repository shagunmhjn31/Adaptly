import pandas as pd
import streamlit as st
from core.session import require_student
from core.style import inject_css
from core.i18n import t
from core.wellbeing import load_factor
from db.database import save_checkin, get_checkins

inject_css()
sid, student = require_student()
st.title(t("ci_title"))
st.caption(t("ci_caption"))

with st.form("ci"):
    mood = st.select_slider(t("ci_mood_q"), options=[1, 2, 3, 4, 5], value=3,
                            format_func=lambda x: t(f"mood_{x}"))
    energy = st.slider(t("ci_energy"), 1, 5, 3)
    note = st.text_input(t("ci_note"))
    ok = st.form_submit_button(t("ci_save"))
if ok:
    save_checkin(sid, mood, energy, note)
    st.success(t("ci_saved"))
    if mood <= 2:
        st.info(t("ci_low"))

factor, stressed = load_factor(sid)
if stressed:
    st.warning(t("ci_stressed"))

with st.expander(t("ci_help")):
    st.write(t("ci_help_text"))

data = get_checkins(sid, 14)
if data:
    df = pd.DataFrame(data)[["day", "mood", "energy"]].sort_values("day").set_index("day")
    st.subheader(t("ci_last14"))
    st.line_chart(df)