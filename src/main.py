#!/usr/bin/env python3

"""Driver."""

import random
from typing import List

from wyrdle.backend import hints as backend_hints
from wyrdle.common import hints, words
from wyrdle.frontend import guess

ROUNDS = 6

def generate_report(word: str, rounds: int, guesses: List[str], hints_: List[hints.Hints]):
    """Print the same report as Wordle."""
    print(f"Wordle {words.possible_words.index(word)} {rounds if guesses[-1] == word else 'X'}/{ROUNDS}\n")
    for round in range(rounds):
        hint = hints_[round + 1]
        tiles = ["⬛"] * words.LENGTH

        for correct_index in hint.inverse_correct:
            tiles[correct_index] = "🟩"

        for misplaced_index in hint.inverse_misplaced:
            tiles[misplaced_index] = "🟨"

        print("".join(tiles))

def main():
    """Driver."""
    word = random.choice(words.possible_words)
    print(f"Chose target word: {word}")

    guesses = []
    hints_ = [hints.Hints()]
    guess_pool = guess.filter_guesses(hints_[0])

    for round in range(ROUNDS):
        print(f"\n==== ROUND {round} ====")

        if round != 0:
            guess_pool &= guess.filter_guesses(hints_[-1]) - {guesses[-1]}

        sorted_guesses = guess.sort_guesses(guess_pool, guess.score_strings())
        if sorted_guesses:
            print(f"Top 5 guesses: {sorted_guesses[:5]}")
        else:
            raise KeyError("No possible guesses?!")

        guesses.append(sorted_guesses[0])
        print(f"(Guessing {guesses[-1]})")

        hints_.append(backend_hints.hint(word, guesses[-1]))
        print(f"Hints: {hints_[-1]}")

        if guesses[-1] == word:
            break
    else:
        print("\n==== FAILURE ====\n")
        generate_report(word, round + 1, guesses, hints_)
        return

    print("\n==== SUCCESS ====\n")
    generate_report(word, round + 1, guesses, hints_)

if __name__ == '__main__':
    main()
