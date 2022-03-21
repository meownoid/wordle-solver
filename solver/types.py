from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class Feedback(Enum):
    CORRECT = auto()
    WRONG_PLACE = auto()
    MISSING = auto()


@dataclass
class WordGuess:
    word: str
    feedback: list[Feedback]


@dataclass
class WordSuggestion:
    word: str
    score: float


class Solver(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def first(self) -> list[WordSuggestion]:
        raise NotImplementedError(
            f"method first is not implemented in the {self.__class__.__name__}"
        )

    @abstractmethod
    def turn(self, guess: WordGuess) -> list[WordSuggestion]:
        raise NotImplementedError(
            f"method turn is not implemented in the {self.__class__.__name__}"
        )
