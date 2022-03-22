import math
import multiprocessing
import random
from itertools import repeat

from solver.simulate import simulate_diff
from solver.space import Space
from solver.types import Solver, WordGuess, WordSuggestion


def _score(word: str, words: list[str]) -> float:
    result = 0

    for target_word in words:
        result += sum(
            map(lambda x: math.log(2 * x + 1), simulate_diff(word, target_word))
        )

    return result / len(words)


class MaxDiffSolver(Solver):
    def __init__(self, words: list[str]) -> None:
        super().__init__()
        self.space = Space(words)

    def _solve(self) -> list[WordSuggestion]:
        cpus = multiprocessing.cpu_count()

        result = []

        words = self.space.words.copy()
        random.shuffle(words)
        words_subset = words[:5000]

        with multiprocessing.Pool(cpus) as pool:
            for word, score in zip(
                words,
                pool.starmap(_score, zip(words, repeat(words_subset)), chunksize=500),
            ):
                result.append(WordSuggestion(word=word, score=score))

        return sorted(result, key=lambda x: -x.score)

    def first(self) -> list[WordSuggestion]:
        words = self.space.words.copy()
        random.shuffle(words)
        return list(map(lambda w: WordSuggestion(word=w, score=1.0), words))

    def turn(self, guess: WordGuess) -> list[WordSuggestion]:
        self.space = self.space.filter(guess)
        return self._solve()
