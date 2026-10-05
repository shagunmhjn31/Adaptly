def evaluate(questions, answers, elapsed_sec):
    per_topic, flags, correct, skipped = {}, [], 0, 0
    for q, a in zip(questions, answers):
        d = per_topic.setdefault(q["topic"], {"correct": 0, "total": 0})
        d["total"] += 1
        if a is None:
            skipped += 1
            flags.append(False)
            continue
        ok = a == q["options"][q["answer"]]
        if ok:
            d["correct"] += 1
            correct += 1
        flags.append(ok)

    n = len(questions)
    h = n // 2
    first = sum(flags[:h]) / max(h, 1)
    second = sum(flags[h:]) / max(n - h, 1)
    return {
        "correct": correct, "total": n, "skipped": skipped,
        "avg_sec": round(elapsed_sec / max(n, 1), 1),
        "first_half": round(first, 2), "second_half": round(second, 2),
        "per_topic": per_topic, "answers": answers,
    }


def behavior_notes(res, lang="English"):
    """Gentle observations only. These are NOT a diagnosis."""
    i = 1 if lang == "Hindi" else 0
    notes = []
    n = res["total"]
    if res["skipped"] > 0.3 * n:
        notes.append(("Many questions were skipped. The topics may be new or time may have run short. "
                      "Starting with easier topics can help.",
                      "Kaafi sawal chhut gaye. Shayad topics naye hain ya time kam pada. "
                      "Easy topics se shuru karna madad karega.")[i])
    if n >= 8 and res["second_half"] < res["first_half"] - 0.3:
        notes.append(("Accuracy dropped toward the end of the test. This can be a sign of tiredness, "
                      "so try shorter sessions with breaks.",
                      "Test ke aakhir mein accuracy kam hui. Ho sakta hai thakaan ho, "
                      "chhote sessions aur breaks try karein.")[i])
    if res["avg_sec"] > 90:
        notes.append(("Each question took quite long. Timed practice quizzes can help build speed.",
                      "Har sawal par kaafi time laga. Timed quizzes se speed badhegi.")[i])
    if not notes:
        notes.append(("Your test pattern looks healthy. Keep it up!",
                      "Aapka test pattern achha raha. Aise hi chalte rahein!")[i])
    return notes