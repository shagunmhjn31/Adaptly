import re
from pypdf import PdfReader
from core.llm import ask_json


def read_pdf(file) -> str:
    reader = PdfReader(file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _offline_topics(text: str):
    """No-AI fallback: split the syllabus into topics with simple rules."""
    names, seen = [], set()
    for line in text.splitlines():
        if ":" in line:
            line = line.split(":", 1)[1]
        for part in re.split(r"[,;•|]", line):
            name = part.strip(" -–.\t")
            if 2 < len(name) <= 60 and name.lower() not in seen:
                seen.add(name.lower())
                names.append(name)
    return [{"name": n, "difficulty": "medium", "est_hours": 2} for n in names[:40]]


def extract_topics(syllabus_text: str):
    prompt = f"""Below is a syllabus. Break it into a list of study topics.
For each topic give: "name", "difficulty" (easy/medium/hard), and "est_hours" (a number).

Return JSON like:
[{{"name": "...", "difficulty": "medium", "est_hours": 3}}]

Syllabus:
{syllabus_text[:12000]}"""
    try:
        topics = ask_json(prompt)
        if isinstance(topics, dict):
            topics = next((v for v in topics.values() if isinstance(v, list)), [])
        topics = [t for t in topics if isinstance(t, dict) and t.get("name")]
        if topics:
            return topics
    except Exception:
        pass
    topics = _offline_topics(syllabus_text)
    if not topics:
        raise ValueError("Syllabus mein topics nahi mile. Topics ko comma ya nayi line se alag karke likho.")
    return topics