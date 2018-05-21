from docx import Document
from docx.shared import RGBColor
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from src.sentence import Sentence
from src.style import POS

import json

PUNCT = {',', '.', '-', "'", '?'}


def rindex(lst, val):
    return len(lst) - 1 - lst[::-1].index(val)


def load_color(rgb):
    return RGBColor(*rgb)


with open('style.json') as f:
    styles = [load_color(style['rgb']) for style in json.load(f).values()]


class Worksheet:
    def __init__(self, lines=[], title='Sentence Worksheet', loc='Worksheet.docx', key=False, font_size=13):
        self.key = key
        self.font_size = font_size
        if key:
            index = loc.rindex('.')
            self.loc = loc[:index] + '(Key)' + loc[index:]
            self.title = title + ' (Key)'
        else:
            self.loc = loc
            self.title = title
        self.font = 'Times New Roman'
        self.lines = [Sentence(line) for line in lines]
        self.doc = Document()

    def render(self):
        self.doc = Document()
        self.add_title(self.title)
        self.add_instructions()
        self.add_title('')
        for line in self.lines:
            self.add_line(line)
        self.format_document()
        self.doc.save(self.loc)

    def add_title(self, text):
        title = self.doc.add_paragraph(text)
        title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        font = title.style.font
        font.name = self.font
        font.size = Pt(16)
        font.bold = True

    def add_instructions(self):
        self.add_instruction('Label: ', 'Subject, Verb, PN, PA, DO, IO, (prepositional phrase)')
        self.add_instruction('Insert ', 'any needed commas, and circle them')

    def add_instruction(self, label, instruction):
        line = self.doc.add_paragraph()
        label = line.add_run(label)
        self.format_run(label, font_size=self.font_size)
        label.bold = True
        self.format_run(line.add_run(instruction), font_size=self.font_size)
        
    def add_line(self, line):
        paragraph = self.doc.add_paragraph(style='List Number')
        self.format_paragraph(paragraph)
        run = None
        current_prep = -1
        if self.key:
            pos = line.pos
        else:
            pos = [None] * len(line.pos)
        for index, (word, color) in enumerate(zip(line.doc, pos)):
            if run is not None and str(word)[0] not in PUNCT:
                run = paragraph.add_run(' ')
                self.format_run(run)
            if type(color) == int:
                if index == current_prep:
                    run = paragraph.add_run(str(word) + ')')
                elif index > current_prep:
                    run = paragraph.add_run('(' + str(word))
                    current_prep = rindex(pos, color)
                else:
                    run = paragraph.add_run(str(word))
            else:
                run = paragraph.add_run(str(word))
            self.format_run(run, color=color)

        if str(line.doc[-1]) not in PUNCT:
            paragraph.add_run('.')

    def format_document(self):
        for section in self.doc.sections:
            section.left_margin = Inches(0.5)
            section.right_margin = Inches(0.5)
            section.top_margin = Inches(0.5)
            section.bottom_margin = Inches(0.5)

    def format_paragraph(self, p):
        p.style.font.bold = False
        p.style.font.size = Pt(self.font_size)
        p.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        style = p.style.paragraph_format
        style.line_spacing = Pt(self.font_size * 3)

    def format_run(self, run, color=None, font_size=13):
        if type(color) == POS:
            run.font.color.rgb = styles[color.value]
        run.bold = False
        run.font.name = self.font
        run.font.size = Pt(font_size)


if __name__ == '__main__':
    sheet = Worksheet(['In the summer, extreme temperatures of over 100 degrees can give visitors heat strokes.',
                       'Big Bend National Park is one of only two national parks in Texas.',
                       'The park looks totally different from the more populated eastern half of the state.',
                       'For about 118 miles, the Rio Grande River runs through the park',
                       "Big Bend's territory extends to the center of the deepest river channel",
                       'The rest of the land on the other side of the channel belongs to Mexico',
                       "The park's climate reaches extreme temperatures",
                       'This park looks totally different from the more populated eastern half of the state'])
    sheet.render()
