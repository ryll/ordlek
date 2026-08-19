# ordfusk

A Swedish word game and a solver that plays it, written in **February–March 2020**.

The format — guess a hidden word, get positional feedback, guess again — goes back
to Jotto (1955), the game show Lingo, and Mastermind before that. It is best known
today as [Wordle](https://en.wikipedia.org/wiki/Wordle), which was released publicly
in October 2021 and went viral the following January. These programs predate that by
about 19 months; they are an independent take on an old format, not on Wordle.

The games use [SAOL](https://svenska.se/) (*Svenska Akademiens ordlista*) as their
dictionary, so everything is played in Swedish.

## The programs

| File | What it is |
| --- | --- |
| `ordlek.py` | The game. Guess a hidden Swedish word of chosen length; correctly placed letters are revealed and stay revealed. Wordle's core loop, minus the yellow "right letter, wrong place" hint — closer to Jotto/Lingo. |
| `mastermindWords.py` | The same idea scored as Mastermind: each guess returns `X` for every letter in the right place and `O` for every letter that appears somewhere else, without saying which is which. |
| `ordfusk.py` | The solver — *fusk* means "cheating". Plays the `ordlek.py` game while ranking every remaining candidate word by two different heuristics, so you can see what an optimal next guess would be. |

## How the solver ranks guesses

`ordfusk.py` keeps the full list of words still consistent with the feedback so far
and counts, for each position, how often every letter of the alphabet occurs across
that candidate set. It then scores candidates two ways:

- **`wordsort`** — scores each word by the RMS deviation of its letters' positional
  frequencies from the midpoint of the candidate set, sorted ascending. A word scores
  well when each of its letters appears in roughly half the remaining candidates, so
  whatever the answer turns out to be, the guess splits the search space near-evenly.
  This is an information-gain heuristic reached arithmetically rather than through
  entropy — the same principle 3Blue1Brown later applied to Wordle in February 2022,
  arrived at here two years earlier by a more roundabout route.
- **`wordsort2`** — scores each word by the mean positional frequency of its letters,
  sorted descending, which simply favours words made of the most likely letters.

Both are printed each round, top five each, so the two strategies can be compared as
the candidate set collapses.

### Known limitation

The pruning only uses positional information: a letter is either in the right place
or eliminated from that position. Guessing that a letter exists *somewhere* in the
word — Wordle's yellow — is collected into the `guessed` sets but never used to filter.
Adding it would cut the candidate set considerably faster. This is left as it was
written in 2020.

## Running

```
python ordlek.py
python mastermindWords.py
python ordfusk.py
```
## Provenance

This repository was originally `python-stuff`, a general Python learning repo started
in January 2020. The word-game files were added in these commits:

- [`708f18e`](https://github.com/ryll/python-stuff/commit/708f18e) — 2020-02-26
- [`d5ec7c3`](https://github.com/ryll/python-stuff/commit/d5ec7c3) — 2020-03-02
- [`e3d8b52`](https://github.com/ryll/python-stuff/commit/e3d8b52) — 2020-03-06
- [`48f6666`](https://github.com/ryll/python-stuff/commit/48f6666) — 2020-03-06

The unrelated exercises that shared the repo (blackjack, tic-tac-toe, Fibonacci,
primes) were removed later; they remain in the history.

Beyond that cleanup the code is unchanged from 2020, apart from three fixes made when
the repo was tidied: restoring `ordfusk.py`'s interactive input (it had been committed
with a hardcoded test word), correcting an input-validation loop that exited instead of
re-prompting on a rejected guess, and adding `__main__` guards.
