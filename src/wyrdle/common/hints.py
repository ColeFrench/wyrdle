"""A module for handling the information the player receives each round."""

from typing import Dict, NamedTuple, Set

class Hints(NamedTuple):
    """A summary of the information the player receives each round."""

    Correct = Dict[str, Set[int]]
    InverseCorrect = Dict[int, str]

    Misplaced = Dict[str, Set[int]]
    InverseMisplaced = Dict[int, Set[str]]

    Absent = Set[str]


    correct: Correct = {}
    inverse_correct: InverseCorrect = {}

    misplaced: Misplaced = {}
    inverse_misplaced: InverseMisplaced = {}

    absent: Absent = set()
