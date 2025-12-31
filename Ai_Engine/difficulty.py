def get_next_difficulty(score: int):
    if score < 3:
        return "basic"
    elif 3 <= score < 7:
        return "intermediate"
    else:
        return "advanced"
