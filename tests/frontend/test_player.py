"""Test the player module."""

import pytest

import wyrdle.frontend.game
import wyrdle.frontend.player

from wyrdle.backend.hint import hint
from wyrdle.common.hint import Hint
from wyrdle.frontend.game import Game
from wyrdle.frontend.guess import filter_guesses

@pytest.fixture
def sleepless(monkeypatch: pytest.MonkeyPatch):
    """Patch sleep to do nothing."""
    # pylint: disable=unused-argument
    def do_nothing(*args, **kwargs):
        """Do nothing."""

    modules_to_patch = (
        wyrdle.frontend.game,
        wyrdle.frontend.player,
    )
    for module in modules_to_patch:
        monkeypatch.setattr(module, 'sleep', do_nothing)

# pylint: disable=redefined-outer-name, unused-argument
def test_bot_repetition(sleepless: None):
    """Ensure the bot doesn't repeat guesses."""
    answer = 'ratty'  # a word where the bot repeats guesses if able
    game = Game(answer=answer, bot=True)
    game.play()

    assert len(game.guesses) == len(set(game.guesses))

def test_bot_absence_conformity(sleepless: None):
    """Ensure the bot doesn't guess letters known to be absent."""
    answer = 'wince'  # a word where the bot guesses an absent letter if able
    game = Game(answer=answer, bot=True)
    game.play()

    hints: list[Hint] = []
    for guess in game.guesses:
        for hint_ in hints:
            assert guess in filter_guesses(hint_)

        hints.append(hint(answer, guess))
