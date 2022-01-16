"""Game player interface and implementations."""

from abc import ABCMeta, abstractmethod

from ..common.hint import Hint

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
