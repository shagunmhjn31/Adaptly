import json, random
from core.llm import ask_json
from core.i18n import lang_rule


def generate_mcqs(topics, n, language="English", difficulty="Medium"):
    prompt = f"""Create {n} multiple-choice questions for a student.
Language rule: {lang_rule(language)} (this applies to questions, options and explanations).
Difficulty: {difficulty}.
Spread the questions across these topics. The "topic" field must be copied exactly from this list
and must NOT be translated:
{json.dumps(topics, ensure_ascii=False)}

Return a JSON list. Each item must look like:
{{"topic": "...", "question": "...", "options": ["...", "...", "...", "..."], "answer": 0, "explanation": "..."}}
"answer" is the index (0-3) of the correct option. Exactly 4 options. Explanation: max 2 short sentences."""
    raw = ask_json(prompt, max_tokens=8000)
    if isinstance(raw, dict):
        raw = next((v for v in raw.values() if isinstance(v, list)), [])

    lower = {t.lower(): t for t in topics}
    questions = []
    for i, q in enumerate(raw):
        try:
            opts = [str(o) for o in q["options"]]
            ans = int(q["answer"])
            if len(opts) != 4 or not 0 <= ans <= 3:
                continue
            correct_text = opts[ans]
            random.shuffle(opts)  # LLMs love putting the answer in the same slot
            topic = lower.get(str(q.get("topic", "")).lower(), topics[i % len(topics)])
            questions.append({
                "topic": topic,
                "question": str(q["question"]),
                "options": opts,
                "answer": opts.index(correct_text),
                "explanation": str(q.get("explanation", "")),
            })
        except Exception:
            continue
    if not questions:
        raise ValueError("The AI did not return questions in the right format. Please try again.")
    return questions