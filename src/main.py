#!/usr/bin/env python3

"""Driver."""

import random

from wordle.backend import hints as backend_hints
from wordle.common import hints, words
from wordle.frontend import guess, hints as frontend_hints

ROUNDS = 6

def main():
    """Driver."""
    word = random.choice(tuple(words.possible_words))
    print(f"Chose target word: {word}")

    guessed = set()
    hint = hints.Hints(correct={}, inverse_correct={},
                       misplaced={}, inverse_misplaced={},
                       absent=set())


    for round in range(ROUNDS):
        print(f"\n==== ROUND {round} ====")

        guess_pool = guess.filter_guesses(hint) - guessed
        if round == ROUNDS - 1:
            # For the final guess, only guess possible answers
            guess_pool -= words.additional_allowed_guesses

        sorted_guesses = guess.sort_guesses(guess_pool, guess.score_strings())
        if sorted_guesses:
            print(f"Top 5 guesses: {sorted_guesses[:5]}")
        else:
            raise KeyError("No possible guesses?!")

        guess_ = sorted_guesses[0]
        guessed.add(guess_)
        print(f"(Guessing {guess_})")
        if guess_ == word:
            break

        frontend_hints.merge(hint, backend_hints.hint(word, guess_))
        print(f"Hints: {hint}")
    else:
        print("\n==== FAILURE ====")
        return

    print("\n==== SUCCESS ====")

if __name__ == '__main__':
    main()
