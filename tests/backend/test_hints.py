"""Test the hint module."""

import pytest

from wyrdle.backend import hint

from .hint import make_hint

_tests = {
    'all correct': (
        ('smile', 'smile', make_hint(correct='smile')),
        ('aaaaa', 'aaaaa', make_hint(correct='aaaaa')),
        ('aabbb', 'aabbb', make_hint(correct='aabbb')),
    ),
    'all misplaced': (
        ('smile', 'limes', make_hint(misplaced='limes')),
        ('aabcc', 'ccaab', make_hint(misplaced='ccaab')),
    ),
    'all absent': (
        ('smile', 'frown', make_hint(absent='frown')),
        ('aaaaa', 'bbbbb', make_hint(absent='bbbbb')),
        ('aabbb', 'cccdd', make_hint(absent='cccdd')),
    ),
    'correct & misplaced': (
        ('smile', 'slime', make_hint(correct='s*i*e', misplaced='*l*m*')),
        ('aaaab', 'aaaba', make_hint(correct='aaa**', misplaced='***ba')),
        ('aabcc', 'ccbaa', make_hint(correct='**b**', misplaced='cc*aa')),
    ),
    'correct & absent': (
        ('smile', 'guile', make_hint(correct='**ile', absent='gu***')),
        ('aaaaa', 'aaaab', make_hint(correct='aaaa*', absent='****b')),
        ('aabbb', 'accbb', make_hint(correct='a**bb', absent='*cc**')),
    ),
    'misplaced & absent': (
        ('smile', 'milky', make_hint(misplaced='mil**', absent='***ky')),
        ('aaaab', 'bbbba', make_hint(misplaced='b***a', absent='*bbb*')),
    ),
    'all': (
        ('smile', 'grins', make_hint(correct='**i**', misplaced='****s', absent='gr*n*')),
        ('aaaab', 'bbaac', make_hint(correct='**aa*', misplaced='b****', absent='*b**c')),
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
