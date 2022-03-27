# Wordle Solver

Simple program for solving the [Wordle](https://www.nytimes.com/games/wordle/index.html) game.

[![asciicast](https://asciinema.org/a/480887.svg)](https://asciinema.org/a/480887)

## Installation

```shell
git clone https://github.com/meownoid/wordle-solver
```

## Usage

```shell
cd wordle-solver
python -m solver
```

## Solvers

1. `random` – randomly suggests words that satisfy all constrains
2. `max-diff` – ranks words based on their difference with all other words that satisfy all constrains
