"""Logic for making guesses."""

import string
from typing import Dict, Set, Tuple

from ..common import words
from ..common.hints import Hints

LetterScores = Dict[str, int]
WordScores = Tuple[LetterScores, ...]

def filter_guesses(hints: Hints) -> Set[str]:
    """Get all possible guesses according to the given hints."""
    filtered_guesses: Set[str] = set()
    for word in words.possible_words | words.additional_allowed_guesses:
        for index, letter in enumerate(word):
            if letter in hints.absent:
                # This letter is absent in the answer, so this is not a
                # possible guess
                break

            if hints.inverse_correct.get(index, letter) != letter \
                    or letter in hints.inverse_misplaced.get(index, set()):
                # This letter is not at this index in the answer, so this is
                # not a possible guess
                break
        else:
            for letter in hints.misplaced:
                if letter not in word:
                    # This letter exists in the answer, so this is not a
                    # possible guess
                    break
            else:
                filtered_guesses.add(word)

    return filtered_guesses

def score_strings() -> WordScores:
    """Score all possible strings, regardless of whether they are permitted guesses.

    Scores are computed for each character in a string, independently of one
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
