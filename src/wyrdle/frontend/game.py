"""Game tracking."""

import random
from string import ascii_lowercase
from time import sleep

from sshkeyboard import listen_keyboard, stop_listening

from ..backend.hint import hint
from ..common.words import LENGTH, allowed_guesses, possible_words
from ..frontend.tile import Position, Style, Tile

# The number of rounds in a game
ROUNDS = 6

class Game:
    """Single instance of a game."""

    def __init__(self, answer: str=random.choice(possible_words)):
        """Create a new game."""
        self.answer = answer
        # Initiate the first guess
        self.guesses = ['']
        self.hints = []
        self.round = 0
        self.index = 0

    def play(self):
        """Play the game from start to finish."""
        self._initialize_board()
        listen_keyboard(on_press=self._handle_keypress, sequential=True, delay_second_char=0.05)

    def _initialize_board(self):
        """Print the initial, empty board."""
        for round_ in range(ROUNDS):
            for index in range(LENGTH):
                tile = Tile(round_, index, position=Position.FIRST_PRINT)
                print(tile, end="")

        print(end="", flush=True)

    def _handle_keypress(self, key: str):
        """Handle the user's input to the game board."""
        if key in ascii_lowercase:
            if self.index < LENGTH:
                # Add the letter to our guess
                self.guesses[-1] += key
                tile = Tile(self.round, self.index, letter=key, position=Position.EDIT)
                print(tile, end="", flush=True)
                self.index += 1
        elif key == 'backspace':
            if self.index > 0:
                # Delete the current letter from our guess
                self.index -= 1
                self.guesses[-1] = self.guesses[-1][:-1]
                tile = Tile(self.round, self.index, position=Position.EDIT)
                print(tile, end="", flush=True)
        elif key == 'enter':
            guess = self.guesses[-1]
            if guess in allowed_guesses:
                # Submit the completed guess
                hint_ = hint(self.answer, guess)
                self.hints.append(hint_)

                for index, letter in enumerate(guess):
                    if index in hint_.inverse_correct:
                        style = Style.CORRECT
                    elif index in hint_.inverse_misplaced:
                        style = Style.MISPLACED
                    elif letter in hint_.absent:
                        style = Style.ABSENT
                    else:
                        raise KeyError(f"expected \"{letter}\" to be absent")

                    tile = Tile(self.round, index, letter=letter, position=Position.EDIT, style=style)
                    print(tile, end="", flush=True)
                    # "Flip" tiles
                    sleep(0.1)

                self.round += 1
                self.index = 0

                if self.round == ROUNDS or guess == self.answer:
                    # Game over
                    stop_listening()
                else:
                    # Initiate the next guess
                    self.guesses.append('')
