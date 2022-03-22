from collections import Counter

from solver.types import Feedback


def simulate_diff(word: str, word_target: str) -> list[Feedback]:
    if len(word) != len(word_target):
        raise ValueError("words must be of the same length")

    word_target_cnt = Counter(word_target)

    result = []

    for w, wt in zip(word, word_target):
        if w == wt:
            result.append(Feedback.CORRECT)
            word_target_cnt[w] -= 1
            continue

        result.append(Feedback.MISSING)

    for i, w in enumerate(word):
        if result[i] == Feedback.CORRECT:
            continue

        if word_target_cnt[w] > 0:
            result[i] = Feedback.WRONG_PLACE
            word_target_cnt[w] -= 1

    return result
