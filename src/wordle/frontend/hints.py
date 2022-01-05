"""A module for processing the information the player receives each round."""

from ..common.hints import Hints

def _merge_correct(current: Hints.Correct, new: Hints.Correct):
    for letter, indices in new.items():
        current.setdefault(letter, set()).update(indices)

def _merge_inverse_correct(current: Hints.InverseCorrect, new: Hints.InverseCorrect):
    for index, letter in new.items():
        current[index] = letter

def _merge_misplaced(current: Hints.Misplaced, new: Hints.Misplaced):
    for letter, indices in new.items():
        current.setdefault(letter, set()).update(indices)

def _merge_inverse_misplaced(current: Hints.InverseMisplaced, new: Hints.InverseMisplaced):
    for index, letters in new.items():
        current.setdefault(index, set()).update(letters)

def _merge_absent(current: Hints.Absent, new: Hints.Absent):
    current |= new

def merge(current: Hints, new: Hints):
    """Merge newly received hints with the current ones."""
    _merge_correct(current.correct, new.correct)
    _merge_inverse_correct(current.inverse_correct, new.inverse_correct)

    _merge_misplaced(current.misplaced, new.misplaced)
    _merge_inverse_misplaced(current.inverse_misplaced, new.inverse_misplaced)

    _merge_absent(current.absent, new.absent)
