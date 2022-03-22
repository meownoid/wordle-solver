import pytest

from solver.simulate import simulate_diff
from solver.types import Feedback


def test_simulate_diff():
    c = Feedback.CORRECT
    w = Feedback.WRONG_PLACE
    m = Feedback.MISSING

    with pytest.raises(ValueError):
        simulate_diff("abc", "ab")

    assert simulate_diff("", "") == []
    assert simulate_diff("a", "a") == [c]
    assert simulate_diff("a", "b") == [m]
    assert simulate_diff("ab", "ba") == [w, w]
    assert simulate_diff("aba", "bac") == [w, w, m]
    assert simulate_diff("aab", "abb") == [c, m, c]
    assert simulate_diff("baba", "caca") == [m, c, m, c]
    assert simulate_diff("a" * 100, "c" * 100) == [m] * 100
    assert simulate_diff("a" * 100, "a" * 100) == [c] * 100
    assert simulate_diff("a" * 100 + "b", "b" + "a" * 100) == [w] + [c] * 99 + [w]
