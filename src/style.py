from enum import Enum
from docx.shared import RGBColor


class POS(Enum):
    Noun = RGBColor(58, 124, 165)  # Blue
    Verb = RGBColor(105, 143, 63)  # Green
    DirectObject = RGBColor(255, 210, 63)  # Yellow
    IndirectObject = RGBColor(211, 78, 36)  # Orange
    PredicateNominative = RGBColor(251, 172, 190)  # Pink
    PredicateAdjective = RGBColor(143, 57, 133)   # Purple
