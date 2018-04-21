from enum import Enum


class POS(Enum):
    Noun = 1
    Verb = 2
    DirectObject = 3
    IndirectObject = 4
    PredicateNominative = 5
    PredicateAdjective = 6
    Punctuation = 7
