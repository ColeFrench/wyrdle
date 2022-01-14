"""Game tracking."""

from datetime import datetime
from string import ascii_lowercase
from time import sleep

from colorama import Style as AnsiStyle
from sshkeyboard import listen_keyboard, stop_listening

from ..backend.hint import hint
from ..common.words import LENGTH, allowed_guesses, possible_words
from ..frontend.tile import Position, Style, Tile

# The number of rounds in a game
ROUNDS = 6

class Game:
    """Single instance of a game."""

    def __init__(self, answer: str=possible_words[(datetime.now() - datetime(2021, 6, 19)).days % len(possible_words)]):
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
        print()
        self._summarize()
        print()
        self._generate_report()

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

    def _summarize(self):
        if self.guesses[-1] == self.answer:
            print(f"{AnsiStyle.BRIGHT}Victory! 🏆{AnsiStyle.RESET_ALL}")
        else:
            print(f"{AnsiStyle.DIM}Defeat 😣{AnsiStyle.RESET_ALL} The word was {AnsiStyle.BRIGHT}{self.answer}{AnsiStyle.RESET_ALL}.")

    def _generate_report(self):
        """Print the same report as Wordle."""
        print(f"Wordle {possible_words.index(self.answer)} {self.round if self.guesses[-1] == self.answer else 'X'}/{ROUNDS}\n")
        for round_ in range(self.round):
            hint_ = self.hints[round_]
            tiles = ["⬛"] * LENGTH

            for correct_index in hint_.inverse_correct:
                tiles[correct_index] = "🟩"

            for misplaced_index in hint_.inverse_misplaced:
                tiles[misplaced_index] = "🟨"

            print("".join(tiles))
