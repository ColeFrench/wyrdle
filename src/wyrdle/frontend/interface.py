"""User interface."""

import colorama
from tap import Tap

from .game import Game

class _ArgumentParser(Tap):
    word: str = 'today\'s'  # which word to make the answer
    bot: bool = False  # have the bot play instead

    def configure(self):
        self.add_argument('-w', '--word')
        self.add_argument('-b', '--bot')

def cli():
    """Command-line interface."""
    args = _ArgumentParser(description="Interact with Wordle.").parse_args()
    game_kwargs = {
        'bot': args.bot,
    }
    if args.word != 'today\'s':
        game_kwargs['answer'] = args.word

    colorama.init()
    Game(**game_kwargs).play()
