"""Hint manipulation for ease of testing."""

from wyrdle.common.hint import Hint
from wyrdle.common.words import LENGTH

_NONMATCHING_CHARACTER = '*'
_DEFAULT_ARGUMENT = _NONMATCHING_CHARACTER * LENGTH

def make_hint(correct: str=_DEFAULT_ARGUMENT,
              misplaced: str=_DEFAULT_ARGUMENT,
              absent: str=_DEFAULT_ARGUMENT) -> Hint:
    """Construct a hint using a simple syntax.

    Each argument is a guess with nonmatching letters replaced by asterisks.

    For example, if 'puppy' is the answer and 'poppy' is the guess, then pass
    `correct='p*ppy'` and `absent='*o***'`.
    """
    constructed_correct = {}
    for index, character in enumerate(correct):
        if character != _NONMATCHING_CHARACTER:
            constructed_correct.setdefault(character, set()).add(index)

    constructed_misplaced = {}
    for index, character in enumerate(misplaced):
        if character != _NONMATCHING_CHARACTER:
            constructed_misplaced.setdefault(character, set()).add(index)

    constructed_absent = set(
        character for character in absent if character != _NONMATCHING_CHARACTER
    )

    return Hint(correct=constructed_correct,
                misplaced=constructed_misplaced,
                absent=constructed_absent)
