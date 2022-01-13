"""User interface."""

import argparse

import colorama

from .game import Game

def cli():
    """Command-line interface."""
    parser = argparse.ArgumentParser(description="Interact with Wordle.")
    parser.parse_args()

    colorama.init()
    Game().play()
