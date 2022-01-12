"""Test the hints module."""

import pytest

from wyrdle.backend import hints

_tests = {
    'all absent': (
        ('smile', 'frown', hints.Hints(absent=set('frown'))),
    ),
    'all misplaced': (
        ('smile', 'limes', hints.Hints(misplaced={v: {k} for k, v in enumerate('limes')})),
    ),
    'all correct': (
        ('smile', 'smile', hints.Hints(correct={v: {k} for k, v in enumerate('smile')})),
    ),
}

@pytest.mark.parametrize(
    argnames=('answer', 'guess', 'expected'),
    argvalues=(test for test_group in _tests.values() for test in test_group),
    ids=(f"{id_}: {answer}; {guess}?" for id_, test_group in _tests.items() for answer, guess, _ in test_group),
)
def test_hints(answer: str, guess: str, expected: hints.Hints):
    """Test that the backend provides the expected hints."""
    assert expected == hints.hint(answer, guess)
