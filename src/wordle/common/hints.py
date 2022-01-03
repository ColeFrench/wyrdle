"""A module for handling the information the player receives each round."""

from typing import Dict, NamedTuple, Set

class Hints(NamedTuple):
    """A summary of the information the player receives each round."""

    Correct = Dict[str, Set[int]]
    Misplaced = Dict[str, Set[int]]
    Absent = Set[str]

    correct: Correct
    misplaced: Misplaced
    absent: Absent

    def _merge_correct(self, new: Correct):
        for letter, indices in new.items():
            self.correct.setdefault(letter, set()).update(indices)

    def _merge_misplaced(self, new: Misplaced):
        for letter, indices in new.items():
            self.misplaced.setdefault(letter, set()).update(indices)

    def _merge_absent(self, new: Absent):
        self.absent.update(new)

    def merge(self, new: 'Hints'):
        """Merge newly received hints with the current ones."""
        self._merge_correct(new.correct)
        self._merge_misplaced(new.misplaced)
        self._merge_absent(new.absent)
