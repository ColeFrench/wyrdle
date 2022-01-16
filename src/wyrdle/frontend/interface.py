"""User interface."""

import colorama
from tap import Tap

from .game import Game

class _ArgumentParser(Tap):
    pass

def cli():
    """Command-line interface."""
    _ArgumentParser(description="Interact with Wordle.").parse_args()

    colorama.init()
    Game().play()
