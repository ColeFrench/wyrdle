"""User interface."""

import colorama
from tap import Tap

from .game import Game

class _ArgumentParser(Tap):
    bot: bool = False  # have the bot play instead

    def configure(self):
        self.add_argument('-b', '--bot')

def cli():
    """Command-line interface."""
    args = _ArgumentParser(description="Interact with Wordle.").parse_args()

    colorama.init()
    Game(bot=args.bot).play()
