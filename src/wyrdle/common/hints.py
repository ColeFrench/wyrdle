"""A module for handling the information the player receives each round."""

from dataclasses import dataclass, field
from typing import Dict, Set

@dataclass
class Hints:
    """A summary of the information the player receives each round."""

    correct: Dict[str, Set[int]] = field(default_factory=dict)
    inverse_correct: Dict[int, str] = field(default_factory=dict)

    misplaced: Dict[str, Set[int]] = field(default_factory=dict)
    inverse_misplaced: Dict[int, Set[str]] = field(default_factory=dict)

    absent: Set[str] = field(default_factory=set)
