"""Test the hint module."""

import pytest

from wyrdle.backend import hint

from .hint import make_hint

_tests = {
    'all correct': (
        ('smile', 'smile', make_hint(correct='smile')),
    ),
    'all misplaced': (
        ('smile', 'limes', make_hint(misplaced='limes')),
    ),
    'all absent': (
        ('smile', 'frown', make_hint(absent='frown')),
    ),
    'correct & misplaced': (
        ('smile', 'slime', make_hint(correct='s*i*e', misplaced='*l*m*')),
    ),
    'correct & absent': (
        ('smile', 'guile', make_hint(correct='**ile', absent='gu***')),
    ),
    'misplaced & absent': (
        ('smile', 'milky', make_hint(misplaced='mil**', absent='***ky')),
    ),
    'all': (
        ('smile', 'grins', make_hint(correct='**i**', misplaced='****s', absent='gr*n*')),
    ),
}

@pytest.mark.parametrize(
    argnames=('answer', 'guess', 'expected'),
    argvalues=(test for test_group in _tests.values() for test in test_group),
    ids=(f"{id_}: {answer}; {guess}?" for id_, test_group in _tests.items() for answer, guess, _ in test_group),
)
def test_hints(answer: str, guess: str, expected: hint.Hint):
    """Test that the backend provides the expected hints."""
    assert expected == hint.hint(answer, guess)
