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
