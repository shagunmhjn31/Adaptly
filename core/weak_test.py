import random
from db.database import latest_topic_scores, missed_topics
from core.mock_test import generate_mcqs

APTITUDE_TOPICS = ["Logical Reasoning", "Numerical Ability"]


def weak_topic_list(sid):
    """Weak = score below 60% OR planned-but-missed recently. Weakest first."""
    scores = latest_topic_scores(sid)
    weak = {t for t, p in scores.items() if p < 60} | set(missed_topics(sid))
    ordered = sorted(weak, key=lambda t: scores.get(t, 50))
    return ordered, scores


def level_for(score):
    """Adaptive difficulty from the student's current score on that topic."""
    if score is None:
        return "Medium"
    if score < 35:
        return "Easy"
    if score < 60:
        return "Medium"
    return "Hard"


def generate_weak_test(topics, scores, n, language, aptitude=False):
    groups = {}
    for t in topics:
        groups.setdefault(level_for(scores.get(t)), []).append(t)
    if aptitude:
        groups.setdefault("Medium", []).extend(APTITUDE_TOPICS)

    total = sum(len(g) for g in groups.values())
    questions, last_err = [], None
    for level, group in groups.items():
        count = max(2, round(n * len(group) / total))
        try:
            questions += generate_mcqs(group, count, language, level)
        except Exception as e:  # one group failing should not kill the test
            last_err = e
    if not questions:
        raise last_err or ValueError("Sawal nahi ban paye.")
    random.shuffle(questions)
    return questions[: n + 2]