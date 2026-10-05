from db.database import get_checkins


def load_factor(sid):
    """If the last 3 check-ins average 2 or below, lighten the plan by 20%."""
    moods = [c["mood"] for c in get_checkins(sid, 3)]
    if len(moods) >= 3 and sum(moods) / len(moods) <= 2.0:
        return 0.8, True
    return 1.0, False