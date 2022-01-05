"""Logic for making guesses."""

import string
from typing import Dict, List, Set

from ..common import words
from ..common.hints import Hints

LetterScores = Dict[str, int]
WordScores = List[LetterScores]

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

    Scores are returned in an arbitrary order. They are computed for each
    character in a string, independently of one another.
    """
    # Initialize scores to 0
    scores = list(dict.fromkeys(string.ascii_lowercase, 0) for _ in range(words.LENGTH))

    for word in words.possible_words:
        for i in range(words.LENGTH):
            scores[i][word[i]] += 1

    for i in range(words.LENGTH):
        for letter in string.ascii_lowercase:
            # Score each character by its frequency's closeness to 50%. This
            # means the best character is the one that eliminates closest to
            # half the possible words. Note that this is only true per
            # character, so there is correlation between characters that is not
            # considered.
            scores[i][letter] = -abs((len(words.possible_words) // 2) - scores[i][letter])

    return scores

def sort_guesses(guesses: Set[str], scores: WordScores) -> List[str]:
    """Sort the given guesses according to the given scores.

    They are returned in nonascending order.
    """
    scored_guesses = {}
    for guess in guesses:
        scored_guesses[guess] = sum(scores[i][guess[i]] for i in range(words.LENGTH))

    sorted_scored_guesses = sorted(scored_guesses.items(), key=lambda item: item[1], reverse=True)
    return [guess for guess, _ in sorted_scored_guesses]
