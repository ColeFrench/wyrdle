"""Test the hint module."""

import pytest

from wyrdle.backend import hint

_tests = {
    'all correct': (
        ('smile', 'smile', hint.Hint(correct={v: {k} for k, v in enumerate('smile')})),
    ),
    'all misplaced': (
        ('smile', 'limes', hint.Hint(misplaced={v: {k} for k, v in enumerate('limes')})),
    ),
    'all absent': (
        ('smile', 'frown', hint.Hint(absent=set('frown'))),
    ),
    'correct & misplaced': (
        ('smile', 'slime', hint.Hint(
            correct={'s': {0}, 'i': {2}, 'e': {4}},
            misplaced={'l': {1}, 'm': {3}}
        )),
    ),
    'correct & absent': (
        ('smile', 'guile', hint.Hint(
            correct={'i': {2}, 'l': {3}, 'e': {4}},
            absent=set('gu')
        )),
    ),
    'misplaced & absent': (
        ('smile', 'milky', hint.Hint(
            misplaced={'m': {0}, 'i': {1}, 'l': {2}},
            absent=set('ky')
        )),
    ),
    'all': (
        ('smile', 'grins', hint.Hint(
            correct={'i': {2}},
            misplaced={'s': {4}},
            absent=set('grn')
        )),
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
