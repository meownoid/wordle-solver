from solver.types import Feedback, WordGuess


class Space:
    def __init__(self, words: list[str]):
        self._words = sorted(set(map(lambda x: x.lower(), words)))
        self._space = self._words

    @property
    def words(self) -> list[str]:
        return self._space

    def filter(self, guess: WordGuess) -> None:
        new_space = []

        letters_missing = set()
        letters_present = set()

        for w, f in zip(guess.word, guess.feedback):
            if f == Feedback.MISSING:
                letters_missing.add(w)
                continue

            letters_present.add(w)

        letters_excluded = letters_missing - letters_present

        for word in self._space:
            word_set = set(word)

            if len(letters_excluded & word_set) > 0:
                continue

            if letters_present and len(letters_present & word_set) == 0:
                continue

            ok = True

            for word_letter, guess_letter, feedback in zip(
                word, guess.word, guess.feedback
            ):
                if feedback == Feedback.CORRECT:
                    if word_letter != guess_letter:
                        ok = False
                        break
                elif feedback == Feedback.WRONG_PLACE:
                    if word_letter == guess_letter:
                        ok = False
                        break

            if not ok:
                continue

            new_space.append(word)

        self._space = new_space
