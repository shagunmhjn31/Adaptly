import re, glob, py_compile, importlib, os, sys

bad = []


def step(name, fn):
    try:
        fn()
        print("OK   ", name)
    except Exception as e:
        bad.append(name)
        print("FAIL ", name, "->", type(e).__name__, str(e)[:160])


# 1) syntax of every file
files = glob.glob("core/*.py") + glob.glob("db/*.py") + glob.glob("pages/*.py") + ["Home.py"]
for f in files:
    step("syntax " + f, lambda f=f: py_compile.compile(f, doraise=True))

# 2) every core module imports
for m in ["llm", "i18n", "session", "style", "auth", "syllabus", "profile", "planner",
          "wellbeing", "diagnostic", "mock_test", "weak_test", "tutor"]:
    step("import core." + m, lambda m=m: importlib.import_module("core." + m))


# 3) every text key used by the pages exists in i18n
def keys_check():
    from core.i18n import STRINGS
    missing = set()
    for f in glob.glob("pages/*.py") + ["Home.py"]:
        for k in re.findall(r'\bt\("([A-Za-z0-9_\-]+)"', open(f, encoding="utf-8").read()):
            if not k.endswith("_") and k not in STRINGS:
                missing.add(f"{k} ({f})")
    if missing:
        raise KeyError("missing i18n keys: " + ", ".join(sorted(missing)[:8]))


step("i18n keys", keys_check)


# 4) database + planner + tests logic on a temporary database
def logic_check():
    import db.database as d
    d.DB_PATH = "check_tmp.db"
    if os.path.exists(d.DB_PATH):
        os.remove(d.DB_PATH)
    d.init_db()
    sid = d.save_student("T", "English", "Exam", "2030-01-01", [{"name": "A"}, {"name": "B"}], 4)
    d.add_goal(sid, "Maths", "Exam", "2030-01-01", 100, 3, 0, "", ["A", "B"])
    d.save_result(sid, "A", 1, 5, "diagnostic")
    d.save_test_session(sid, "diagnostic", 5, 1, 30, 0, 0.2, 0.2)
    d.save_checkin(sid, 3, 3, "")
    d.log_study(sid, "2030-01-01", "Maths", "A", 60, 0)
    from core.planner import plan_for
    from core.weak_test import weak_topic_list
    from core.tutor import build_context
    from core.diagnostic import evaluate, behavior_notes
    plan_for(sid)
    weak_topic_list(sid)
    build_context(sid)
    q = [{"topic": "A", "options": ["x", "y", "z", "w"], "answer": 0}]
    behavior_notes(evaluate(q, ["x"], 10))


step("database + planner + tests", logic_check)
try:
    os.remove("check_tmp.db")
except Exception:
    pass


# 5) AI call (only if you run: python check.py ai)
def ai_check():
    from core.llm import chat
    from core.mock_test import generate_mcqs
    chat([{"role": "user", "content": "Say hi"}])
    generate_mcqs(["Ohm law", "Matrices"], 4)


if "ai" in sys.argv:
    step("AI chat + question generation", ai_check)

print("\nALL GOOD" if not bad else f"\n{len(bad)} problem(s). Send me the FAIL lines above.")