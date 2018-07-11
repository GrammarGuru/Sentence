from enum import Enum
import json


class POS(Enum):
    Noun = 0  # Blue
    Verb = 1  # Green
    DirectObject = 2  # Yellow
    IndirectObject = 3  # Orange
    PredicateNominative = 4  # Pink
    PredicateAdjective = 5   # Purple
    PrepositionalPhrase = 6
    Appositive = 7
    Participle = 8
    Infinitive = 9
