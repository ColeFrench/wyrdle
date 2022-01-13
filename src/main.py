#!/usr/bin/env python3

"""Driver."""

import random

from wyrdle.backend import hint as backend_hint
from wyrdle.common import hint, words
from wyrdle.frontend import guess

ROUNDS = 6

def generate_report(word: str, rounds: int, guesses: list[str], hints: list[hint.Hint]):
    """Print the same report as Wordle."""
    print(f"Wordle {words.possible_words.index(word)} {rounds if guesses[-1] == word else 'X'}/{ROUNDS}\n")
    for round in range(rounds):
        hint_ = hints[round + 1]
        tiles = ["⬛"] * words.LENGTH

        for correct_index in hint_.inverse_correct:
            tiles[correct_index] = "🟩"

        for misplaced_index in hint_.inverse_misplaced:
            tiles[misplaced_index] = "🟨"

        print("".join(tiles))

def main():
    """Driver."""
    word = random.choice(words.possible_words)
    print(f"Chose target word: {word}")

    guesses = []
    hints = [hint.Hint()]
    guess_pool = guess.filter_guesses(hints[0])

    for round in range(ROUNDS):
        if round != 0:
            guess_pool &= guess.filter_guesses(hints[-1]) - {guesses[-1]}

        sorted_guesses = guess.sort_guesses(guess_pool, guess.score_strings())
        if not sorted_guesses:
            raise KeyError("No possible guesses?!")

        guesses.append(sorted_guesses[0])
        hints.append(backend_hint.hint(word, guesses[-1]))

        if guesses[-1] == word:
            break
    else:
        print("\n==== FAILURE ====\n")
        generate_report(word, round + 1, guesses, hints)
        return

    print("\n==== SUCCESS ====\n")
    generate_report(word, round + 1, guesses, hints)

if __name__ == '__main__':
    main()
