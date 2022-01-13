"""Game tracking."""

import random

from colorama import Back, Cursor, Fore, Style

from ..backend.hint import hint
from ..common.words import LENGTH, possible_words

class Game:
    """Single instance of a game."""

    # The number of rounds in a game
    rounds = 6

    def __init__(self, answer: str=random.choice(possible_words)):
        """Create a new game."""
        self.answer = answer
        self.guesses = []
        self.hints = []

    def play(self):
        """Play the game from start to finish."""
        for round_ in range(self.rounds):
            self.play_round(round_)
            if self.answer == self.guesses[-1]:
                break

    def play_round(self, round_: int):
        """Play a round of the game."""
        prompt = f"Round {round_ + 1}/{self.rounds}: "
        guess = input(prompt)
        self.guesses.append(guess)

        hint_ = hint(self.answer, guess)
        self.hints.append(hint_)

        colors = [Fore.WHITE + Back.BLACK] * LENGTH

        for correct_index in hint_.inverse_correct:
            colors[correct_index] = Fore.BLACK + Back.GREEN

        for misplaced_index in hint_.inverse_misplaced:
            colors[misplaced_index] = Fore.BLACK + Back.YELLOW

        annotated_guess = Style.BRIGHT \
                        + ''.join(color + guess for color, guess in zip(colors, guess)) \
                        + Style.RESET_ALL

        print(f"{Cursor.UP()}{Cursor.FORWARD(len(prompt))}{annotated_guess}")
