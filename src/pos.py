from enum import Enum
import json


class POS(Enum):
    Noun = 0  # Blue
    Verb = 1  # Green
    DirectObject = 2  # Yellow
    IndirectObject = 3  # Orange
    PredicateNominative = 4  # Pink
    PredicateAdjective = 5   # Purple
    Appositive = 6
    Participle = 7
    Infinitive = 8
