import random

from solver.space import Space
from solver.types import Solver, WordGuess, WordSuggestion


class RandomSolver(Solver):
    def __init__(self, words: list[str]) -> None:
        super().__init__()
        self.space = Space(words)

    def _solve(self) -> list[WordSuggestion]:
        words = self.space.words.copy()
        random.shuffle(words)
        return list(map(lambda w: WordSuggestion(word=w, score=1.0), words))

    def first(self) -> list[WordSuggestion]:
        return self._solve()

    def turn(self, guess: WordGuess) -> list[WordSuggestion]:
        self.space = self.space.filter(guess)
        return self._solve()
