"""A module for administering the information the player receives each round."""

from ..common.hints import Hints

def hint(answer: str, guess: str) -> Hints:
    """Hint at the answer based on a guess."""
    hint = Hints({}, {}, set())
    working_answer = answer[:]

    for guess_index, letter in enumerate(guess):
        try:
            answer_index = working_answer.index(letter)
        except ValueError:  # "Absent"
            hint.absent.add(letter)
            continue

        # The letter is present. Let's remove it from the answer so we don't
        # match this specific occurrence again. We should replace it with an
        # unmatchable character rather than remove it outright, since we want
        # to preserve the locations of other letters.
        working_answer = working_answer[:answer_index] \
                       + ' ' \
                       + working_answer[answer_index + 1:]

        if guess_index == answer_index:  # "Correct"
            hint.correct[letter] = guess_index
        else:  # "Misplaced"
            hint.misplaced[letter] = guess_index

    return hint
