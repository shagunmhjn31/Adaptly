import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    :root { --violet:#7C74FF; --blue:#3B82F6; --cyan:#22D3EE; --pink:#F472B6;
            --amber:#FBBF24; --green:#34D399; --card:rgba(255,255,255,.05); --line:#2A2F4A; }
    html, body, .stApp, [class*="css"] { font-family:'Poppins',sans-serif; }

    .stApp {
        background:
            radial-gradient(900px 500px at 5% -5%, rgba(124,116,255,.28), transparent 60%),
            radial-gradient(800px 460px at 100% 5%, rgba(244,114,182,.18), transparent 55%),
            radial-gradient(900px 500px at 50% 110%, rgba(34,211,238,.14), transparent 60%),
            #0A0D18;
    }
    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer, .stAppDeployButton { visibility:hidden; display:none; }
    .block-container { max-width:1150px; padding-top:1.6rem; padding-bottom:4rem; }

    /* sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,#12163A 0%,#0C0F22 100%); border-right:1px solid var(--line);
    }
    [data-testid="stSidebarNav"] a { border-radius:12px; margin:3px 8px; padding:7px 12px; transition:.15s; }
    [data-testid="stSidebarNav"] a:hover { background:rgba(124,116,255,.18); transform:translateX(3px); }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background:linear-gradient(135deg,var(--violet),var(--blue)); font-weight:700; color:#fff;
    }

    /* headings: colored underline accent on every page title */
    h1 { font-weight:800; letter-spacing:-.5px; }
    h1::after { content:""; display:block; width:96px; height:5px; border-radius:99px; margin-top:10px;
        background:linear-gradient(90deg,var(--violet),var(--cyan),var(--pink)); }
    h2, h3 { font-weight:700; }

    /* hero */
    .hero {
        background:linear-gradient(120deg,#7C74FF,#3B82F6,#22D3EE,#F472B6);
        background-size:300% 300%; animation:flow 12s ease infinite;
        padding:38px 34px; border-radius:24px; margin-bottom:22px;
        box-shadow:0 20px 60px rgba(124,116,255,.35);
    }
    @keyframes flow { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
    .hero h1 { margin:0; color:#fff; font-size:2.7rem; }
    .hero h1::after { display:none; }
    .hero p { margin:8px 0 0; color:#fff; opacity:.92; font-size:1.1rem; }

    /* feature cards, each with its own color */
    .feat-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:16px; margin:14px 0 24px; }
    .feat { --c:var(--violet); background:var(--card); border:1px solid var(--line);
        border-top:4px solid var(--c); border-radius:20px; padding:20px; transition:.2s; }
    .feat:nth-child(1){--c:#7C74FF} .feat:nth-child(2){--c:#22D3EE} .feat:nth-child(3){--c:#F472B6}
    .feat:nth-child(4){--c:#FBBF24} .feat:nth-child(5){--c:#34D399} .feat:nth-child(6){--c:#FB7185}
    .feat:hover { transform:translateY(-5px); border-color:var(--c); box-shadow:0 14px 36px color-mix(in srgb, var(--c) 30%, transparent); }
    .feat .ico { width:48px; height:48px; border-radius:14px; display:flex; align-items:center;
        justify-content:center; font-size:1.6rem; background:color-mix(in srgb, var(--c) 22%, transparent); }
    .feat h4 { margin:12px 0 4px; font-size:1.05rem; font-weight:700; }
    .feat p { margin:0; color:#B4BAD6; font-size:.9rem; line-height:1.5; }

    .pill { display:inline-block; padding:5px 14px; border-radius:999px; font-size:.82rem; font-weight:500;
        background:linear-gradient(135deg,rgba(124,116,255,.28),rgba(34,211,238,.2)); color:#E3E1FF; margin:0 8px 8px 0; }

    /* metrics */
    div[data-testid="stMetric"] { background:var(--card); border:1px solid var(--line);
        border-left:5px solid var(--violet); padding:16px; border-radius:16px; }
    div[data-testid="stColumn"]:nth-child(2) div[data-testid="stMetric"] { border-left-color:var(--cyan); }
    div[data-testid="stColumn"]:nth-child(3) div[data-testid="stMetric"] { border-left-color:var(--pink); }
    div[data-testid="stColumn"]:nth-child(4) div[data-testid="stMetric"] { border-left-color:var(--amber); }
    div[data-testid="stColumn"]:nth-child(5) div[data-testid="stMetric"] { border-left-color:var(--green); }
    div[data-testid="stMetricValue"] { font-weight:800; }

    /* buttons */
    .stButton > button, div[data-testid="stFormSubmitButton"] > button, a[data-testid="stPageLink-NavLink"] {
        border-radius:14px; font-weight:600; padding:.6rem 1.3rem; border:1px solid #343B5E; transition:.15s; }
    .stButton > button:hover { border-color:var(--cyan); transform:translateY(-2px); }
    div[data-testid="stFormSubmitButton"] > button {
        background:linear-gradient(135deg,var(--violet),var(--blue),var(--cyan)); color:#fff; border:none; }
    div[data-testid="stFormSubmitButton"] > button:hover { filter:brightness(1.12); transform:translateY(-2px); }
    a[data-testid="stPageLink-NavLink"] { background:var(--card); }
    a[data-testid="stPageLink-NavLink"]:hover { border-color:var(--pink); background:rgba(244,114,182,.1); }

    /* forms, inputs, tabs */
    div[data-testid="stForm"] { border-radius:20px; border:1px solid var(--line);
        background:var(--card); padding:1.4rem; backdrop-filter:blur(6px); }
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input,
    div[data-baseweb="select"] > div { border-radius:12px !important; }
    button[data-baseweb="tab"] { font-weight:600; padding:10px 20px; }

    /* expanders, alerts, tables, chat */
    details[data-testid="stExpander"] { border-radius:16px; border:1px solid var(--line); background:var(--card); }
    div[data-testid="stAlert"] { border-radius:14px; }
    div[data-testid="stDataFrame"] { border-radius:14px; overflow:hidden; border:1px solid var(--line); }
    div[data-testid="stChatMessage"] { background:var(--card); border:1px solid var(--line);
        border-radius:18px; padding:12px 16px; }
    </style>
    """, unsafe_allow_html=True)