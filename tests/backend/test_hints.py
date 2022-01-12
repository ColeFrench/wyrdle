"""Test the hints module."""

import pytest

from wyrdle.backend import hints

_tests = {
    'all correct': (
        ('smile', 'smile', hints.Hints(correct={v: {k} for k, v in enumerate('smile')})),
    ),
    'all misplaced': (
        ('smile', 'limes', hints.Hints(misplaced={v: {k} for k, v in enumerate('limes')})),
    ),
    'all absent': (
        ('smile', 'frown', hints.Hints(absent=set('frown'))),
    ),
    'correct & misplaced': (
        ('smile', 'slime', hints.Hints(
            correct={'s': {0}, 'i': {2}, 'e': {4}},
            misplaced={'l': {1}, 'm': {3}}
        )),
    ),
    'correct & absent': (
        ('smile', 'guile', hints.Hints(
            correct={'i': {2}, 'l': {3}, 'e': {4}},
            absent=set('gu')
        )),
    ),
    'misplaced & absent': (
        ('smile', 'milky', hints.Hints(
            misplaced={'m': {0}, 'i': {1}, 'l': {2}},
            absent=set('ky')
        )),
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
