"""Game player interface and implementations."""

from abc import ABCMeta, abstractmethod
from queue import Queue
from threading import Thread

from sshkeyboard import listen_keyboard, stop_listening

from ..common.hint import Hint
from . import game

class Player(metaclass=ABCMeta):
    """A player of the game."""

    @abstractmethod
    def start_guess(self, round_: int, hint: Hint) -> None:
        """Start a new guess.

        :param round_: the round that's starting
        :param hint: the hint resulting from the previous guess
        """

    @abstractmethod
    def propose_letter(self, index: int) -> str:
        """Propose the next letter of the current guess.

        :param index: the index of the letter to propose
        """

    @abstractmethod
    def stop_guess(self, round_: int) -> None:
        """Conclude the current guess; it has been submitted.

        :param round_: the round that finished
        """

class User(Player):
    """A human—or chimpanzee… maybe even a corvid?—player."""

    def __init__(self):
        self._thread: Thread = None
        self._queue: Queue[str] = Queue()

    def start_guess(self, round_: int, hint: Hint) -> None:
        if round_ == 0:
            self._start_listening()

    def propose_letter(self, index: int) -> str:
        return self._queue.get()

    def stop_guess(self, round_: int) -> None:
        if round_ == game.ROUNDS - 1:
            self._stop_listening()

    def _start_listening(self) -> None:
        """Start listening to the user's keyboard in a new thread."""
        self._thread = Thread(
            target=listen_keyboard,
            kwargs={
                'on_press': self._handle_keypress,
                'delay_second_char': 0.05,
            },
            daemon=True,
        )
        self._thread.start()

    def _stop_listening(self) -> None:
        """Stop listening to the user's keyboard."""
        stop_listening()

    def _handle_keypress(self, key: str) -> None:
        """Handle the user's input."""
        self._queue.put(key)
