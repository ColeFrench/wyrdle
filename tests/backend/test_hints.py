"""Test the hints module."""

from wyrdle.backend import hints

_tests = {
    # unique letters
    'smile': {
        # all absent letters
        'frown': hints.Hints(
            absent=set('frown'),
        ),
        # all misplaced letters
        'limes': hints.Hints(
            misplaced={v: {k} for k, v in enumerate('limes')},
        ),
        # all correct letters
        'smile': hints.Hints(
            correct={v: {k} for k, v in enumerate('smile')},
        ),
    },
}

def _test_hints(answer: str):
    """Test that the backend provides correct hints for the given answer."""
    for guess, expected_hint in _tests[answer].items():
        assert expected_hint == hints.hint(answer, guess)

def test_unique():
    """Test that the backend provides correct hints when all letters in the answer are unique."""
    _test_hints('smile')
