from enum import Enum
from docx.shared import RGBColor


class POS(Enum):
    Noun = RGBColor(58, 124, 165)
    Verb = RGBColor(105, 143, 63)
    DirectObject = RGBColor(255, 210, 63)
    IndirectObject = RGBColor(211, 78, 36)
    PredicateNominative = RGBColor(251, 172, 190)
    PredicateAdjective = RGBColor(143, 57, 133)
