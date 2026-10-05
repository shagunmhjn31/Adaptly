import sqlite3, json
from datetime import datetime, date, timedelta

DB_PATH = "adaptly.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, language TEXT, exam_name TEXT, exam_date TEXT,
            topics TEXT, weak_topics TEXT, study_hours_per_day REAL
        );
        CREATE TABLE IF NOT EXISTS profiles (
            student_id INTEGER PRIMARY KEY, traits TEXT, summary TEXT
        );
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER, name TEXT, kind TEXT, deadline TEXT,
            marks REAL, difficulty INTEGER, covered INTEGER,
            weaknesses TEXT, topics TEXT
        );
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER, topic TEXT, correct INTEGER, total INTEGER,
            source TEXT, ts TEXT
        );
        CREATE TABLE IF NOT EXISTS test_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER, ts TEXT, mode TEXT, n INTEGER, correct INTEGER,
            avg_sec REAL, skipped INTEGER, first_half REAL, second_half REAL
        );
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER, day TEXT, mood INTEGER, energy INTEGER, note TEXT,
            UNIQUE(student_id, day)
        );
        CREATE TABLE IF NOT EXISTS study_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER, day TEXT, goal_name TEXT, topic TEXT,
            planned INTEGER, done INTEGER,
            UNIQUE(student_id, day, goal_name)
        );
    """)
    try:  # old databases: add the topics column
        conn.execute("ALTER TABLE goals ADD COLUMN topics TEXT")
    except sqlite3.OperationalError:
        pass
    for col in ("username TEXT", "pw_hash TEXT", "salt TEXT"):  # login columns
        try:
            conn.execute(f"ALTER TABLE students ADD COLUMN {col}")
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()


# ---------- students ----------
def save_student(name, language, exam_name, exam_date, topics, hours):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO students (name, language, exam_name, exam_date, topics, weak_topics, study_hours_per_day) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, language, exam_name, str(exam_date), json.dumps(topics), json.dumps([]), hours),
    )
    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return sid


def list_students():
    conn = get_conn()
    rows = conn.execute("SELECT id, name FROM students ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_student(sid):
    conn = get_conn()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (sid,)).fetchone()
    conn.close()
    if not row:
        return None
    s = dict(row)
    s["topics"] = json.loads(s["topics"] or "[]")
    s["weak_topics"] = json.loads(s["weak_topics"] or "[]")
    return s


def set_weak_topics(sid, weak):
    conn = get_conn()
    conn.execute("UPDATE students SET weak_topics = ? WHERE id = ?", (json.dumps(weak), sid))
    conn.commit()
    conn.close()


# ---------- login ----------
def username_taken(username):
    conn = get_conn()
    row = conn.execute("SELECT 1 FROM students WHERE lower(username) = lower(?)",
                       (username,)).fetchone()
    conn.close()
    return row is not None


def set_credentials(sid, username, pw_hash, salt):
    conn = get_conn()
    conn.execute("UPDATE students SET username = ?, pw_hash = ?, salt = ? WHERE id = ?",
                 (username, pw_hash, salt, sid))
    conn.commit()
    conn.close()


def get_credentials(username):
    conn = get_conn()
    row = conn.execute("SELECT id, pw_hash, salt FROM students WHERE lower(username) = lower(?)",
                       (username,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ---------- personality profile ----------
def save_profile(student_id, traits, summary):
    conn = get_conn()
    conn.execute("INSERT OR REPLACE INTO profiles (student_id, traits, summary) VALUES (?, ?, ?)",
                 (student_id, json.dumps(traits), summary))
    conn.commit()
    conn.close()


def get_profile(student_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM profiles WHERE student_id = ?", (student_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return {"traits": json.loads(row["traits"]), "summary": row["summary"]}


# ---------- goals ----------
def add_goal(student_id, name, kind, deadline, marks, difficulty, covered, weaknesses, topics=None):
    conn = get_conn()
    conn.execute(
        "INSERT INTO goals (student_id, name, kind, deadline, marks, difficulty, covered, weaknesses, topics) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (student_id, name, kind, str(deadline), marks, difficulty, covered, weaknesses,
         json.dumps(topics or [])),
    )
    conn.commit()
    conn.close()


def get_goals(student_id):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM goals WHERE student_id = ?", (student_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_goal_progress(goal_id, covered):
    conn = get_conn()
    conn.execute("UPDATE goals SET covered = ? WHERE id = ?", (covered, goal_id))
    conn.commit()
    conn.close()


def delete_goal(goal_id):
    conn = get_conn()
    conn.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()


# ---------- tests ----------
def _now():
    return datetime.now().isoformat(timespec="seconds")


def save_result(sid, topic, correct, total, source):
    conn = get_conn()
    conn.execute("INSERT INTO test_results (student_id, topic, correct, total, source, ts) VALUES (?,?,?,?,?,?)",
                 (sid, topic, correct, total, source, _now()))
    conn.commit()
    conn.close()


def save_test_session(sid, mode, n, correct, avg_sec, skipped, first_half, second_half):
    conn = get_conn()
    conn.execute(
        "INSERT INTO test_sessions (student_id, ts, mode, n, correct, avg_sec, skipped, first_half, second_half) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        (sid, _now(), mode, n, correct, avg_sec, skipped, first_half, second_half))
    conn.commit()
    conn.close()


def get_test_sessions(sid):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM test_sessions WHERE student_id = ? ORDER BY id", (sid,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def latest_topic_scores(sid):
    """Topic -> % score, using the last 3 attempts of each topic."""
    conn = get_conn()
    rows = conn.execute("SELECT topic, correct, total FROM test_results WHERE student_id = ? ORDER BY id",
                        (sid,)).fetchall()
    conn.close()
    by_topic = {}
    for r in rows:
        by_topic.setdefault(r["topic"], []).append((r["correct"], r["total"]))
    out = {}
    for t, attempts in by_topic.items():
        last = attempts[-3:]
        c, n = sum(a[0] for a in last), sum(a[1] for a in last)
        if n:
            out[t] = round(c / n * 100)
    return out


# ---------- wellbeing ----------
def save_checkin(sid, mood, energy, note):
    conn = get_conn()
    conn.execute("INSERT OR REPLACE INTO checkins (student_id, day, mood, energy, note) VALUES (?,?,?,?,?)",
                 (sid, date.today().isoformat(), mood, energy, note))
    conn.commit()
    conn.close()


def get_checkins(sid, limit=14):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM checkins WHERE student_id = ? ORDER BY day DESC LIMIT ?",
                        (sid, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------- study log ----------
def log_study(sid, day, goal_name, topic, planned, done):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO study_log (student_id, day, goal_name, topic, planned, done) VALUES (?,?,?,?,?,?)",
        (sid, str(day), goal_name, topic, planned, done))
    conn.commit()
    conn.close()


def get_study_log(sid):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM study_log WHERE student_id = ? ORDER BY day", (sid,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def missed_topics(sid, days=3):
    """Topics planned but not done in the last few days (they get priority in the new plan)."""
    today = date.today()
    start = (today - timedelta(days=days)).isoformat()
    conn = get_conn()
    rows = conn.execute(
        "SELECT DISTINCT topic FROM study_log WHERE student_id = ? AND planned > 0 AND done = 0 "
        "AND day < ? AND day >= ? AND topic != 'General study'",
        (sid, today.isoformat(), start)).fetchall()
    conn.close()
    return [r["topic"] for r in rows]