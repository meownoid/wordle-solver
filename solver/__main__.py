import argparse
import os
import sys

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


def run_interactive(solver: Solver, n_suggestions: int) -> None:
    print(WELCOME_MESSAGE.strip() + "\n")
    print(f"Using the {solver.__class__.__name__}\n")

    suggestions = solver.first()

    while True:
        if not suggestions:
            print("There are no suggestions!")
            break

        print("Suggestions:\n")
        for sgs in suggestions[:n_suggestions]:
            print(f"- {sgs.word} ({sgs.score:.2f})")

        print("")

        print("Your word:\n> ", end="")
        word = input()
        if word == "q":
            break

        print("")

        suggestions = solver.turn(parse_user_input(word))


def main() -> None:
    parser = argparse.ArgumentParser(description="Wordle solver")
    parser.add_argument(
        "--words-file",
        dest="words_file",
        help="File with list of words (newline separated)",
        default="words.txt",
    )
    parser.add_argument(
        "--solver", dest="solver", help="Solver name", default="max-diff"
    )
    parser.add_argument(
        "--suggestions",
        dest="suggestions",
        help="Number of suggestions to show",
        type=int,
        default=10,
    )

    args = parser.parse_args()

    if not os.path.exists(args.words_file):
        print(f"{args.words_file} does not exist")
        sys.exit(1)

    with open(args.words_file, "r") as f:
        words = f.read().split()

    words = sorted(filter(lambda x: len(x) == 5, map(lambda x: x.lower(), words)))

    if not words:
        print("Word list is empty")
        sys.exit(1)

    if args.solver not in solvers:
        print(f"There is no solver named {args.solver}")
        print(f"Available solvers: {list(solvers.keys())}")
        sys.exit(1)

    solver = solvers[args.solver](words)
    run_interactive(solver, n_suggestions=args.suggestions)


if __name__ == "__main__":
    main()
