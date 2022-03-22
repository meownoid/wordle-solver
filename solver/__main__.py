from solver.solvers import solvers
from solver.types import Feedback, Solver, WordGuess

WELCOME_MESSAGE = """
Hello! Welcome to the Wordle Solver!
Type "q" to quit.
Use "+" if the letter is correct and "?" if the letter is in the wrong place.

Examples:

> crane
> pape?r+
> t+utor+
> t+h+e+i+r+
"""


def parse_user_input(word: str) -> WordGuess:
    letters = []
    feedback = []

    for w in word:
        if w == "+":
            feedback.pop()
            feedback.append(Feedback.CORRECT)
            continue

        if w == "?":
            feedback.pop()
            feedback.append(Feedback.WRONG_PLACE)
            continue

        letters.append(w)
        feedback.append(Feedback.MISSING)

    return WordGuess(word="".join(letters), feedback=feedback)


def run_interactive(solver: Solver) -> None:
    print(WELCOME_MESSAGE.strip() + "\n")
    print(f"Using the {solver.__class__.__name__}\n")

    suggestions = solver.first()

    while True:
        if not suggestions:
            print("There are no suggestions!")
            break

        print("Suggestions:\n")
        for sgs in suggestions[:15]:
            print(f"- {sgs.word} ({sgs.score:.2f})")

        print("")

        print("Your word:\n> ", end="")
        word = input()
        if word == "q":
            break

        print("")

        suggestions = solver.turn(parse_user_input(word))


def main() -> None:
    with open("words.txt", "r") as f:
        words = f.read().split()

    words = sorted(filter(lambda x: len(x) == 5, map(lambda x: x.lower(), words)))

    if not words:
        raise ValueError("Words list is empty")

    solver = solvers["max-diff"](words)
    run_interactive(solver)


if __name__ == "__main__":
    main()
