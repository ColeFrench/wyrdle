"""A module for processing the information the player receives each round."""

from ..common.hints import Hints

def _merge_correct(current: Hints.Correct, new: Hints.Correct):
    for letter, indices in new.items():
        current.setdefault(letter, set()).update(indices)

def _merge_misplaced(current: Hints.Misplaced, new: Hints.Misplaced):
    for letter, indices in new.items():
        current.setdefault(letter, set()).update(indices)

def _merge_absent(current: Hints.Absent, new: Hints.Absent):
    current.update(new)

def merge(current: Hints, new: Hints):
    """Merge newly received hints with the current ones."""
    _merge_correct(current.correct, new.correct)
    _merge_misplaced(current.misplaced, new.misplaced)
    _merge_absent(current.absent, new.absent)
