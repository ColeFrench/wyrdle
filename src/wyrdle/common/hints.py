"""A module for handling the information the player receives each round."""

from dataclasses import dataclass, field
from typing import Dict, Set

@dataclass
class Hints:
    """A summary of the information the player receives each round."""

    correct: Dict[str, Set[int]] = field(default_factory=dict)
    inverse_correct: Dict[int, str] = field(default_factory=dict, init=False)

    misplaced: Dict[str, Set[int]] = field(default_factory=dict)
    inverse_misplaced: Dict[int, Set[str]] = field(default_factory=dict, init=False)

    absent: Set[str] = field(default_factory=set)

    def __post_init__(self):
        """Initialize inverse mappings."""
        for letter, indices in self.correct.items():
            for index in indices:
                self.inverse_correct[index] = letter

        for letter, indices in self.misplaced.items():
            for index in indices:
                self.inverse_misplaced.setdefault(index, set()).add(letter)
