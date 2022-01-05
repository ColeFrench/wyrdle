"""Logic for making guesses."""

import string
from typing import Dict, Tuple

from ..common import words

LetterScores = Dict[str, int]
WordScores = Tuple[LetterScores, ...]

def score_guesses() -> WordScores:
    """Score all possible guesses.

    Scores are computed for each character in a guess, independently of one
    another. They are returned sorted in nonascending order.
    """
    # Initialize scores to 0
    scores = tuple(dict.fromkeys(string.ascii_lowercase, 0) for _ in range(words.LENGTH))

    for word in words.possible_words:
        for i in range(words.LENGTH):
            scores[i][word[i]] += 1

    for word in words.possible_words:
        for i in range(words.LENGTH):
            # Score each character by its frequency's closeness to 50%. This
            # means the best character is the one that eliminates closest to
            # half the possible words. Note that this is only true per
            # character, so there is correlation between characters that is not
            # considered.
            scores[i][word[i]] = abs((len(words.possible_words) // 2) - scores[i][word[i]])

    # Sort scores in nonascending order
    sorted_scores = tuple(dict(sorted(letter_scores.items(), key=lambda item: item[1], reverse=True)) for letter_scores in scores)
    return sorted_scores
