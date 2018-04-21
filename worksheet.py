from docx import Document
from sentence import Sentence
from docx.shared import Pt
from style import POS

PUNCT = {',', '.', '-', "'"}


def rindex(lst, val):
    return len(lst) - 1 - lst[::-1].index(val)

class Worksheet:
    def __init__(self, lines, title='Sentence Worksheet'):
        self.title = title
        self.lines = [Sentence(line) for line in lines]
        self.doc = Document()

    def render(self):
        for line in self.lines:
            self._add_line(line)
        self.doc.save(self.title + '.docx')

    def _add_line(self, line):
        paragraph = self.doc.add_paragraph()
        paragraph.style = 'List Number'
        self._format_paragraph(paragraph)
        run = None
        current_prep = -1
        for index, (word, color) in enumerate(zip(line.doc, line.pos)):
            if run is not None and str(word) not in PUNCT:
                run = paragraph.add_run(' ')
                self._format_run(run)
            if type(color) == int:
               if index == current_prep:
                   run = paragraph.add_run(str(word) + ')')
               elif index > current_prep:
                   run = paragraph.add_run('(' + str(word))
                   current_prep = rindex(line.pos, color)
               else:
                   run = paragraph.add_run(str(word))
            else:
                run = paragraph.add_run(str(word))
            self._format_run(run, color=color)

        if str(line.doc[-1]) != '.':
            paragraph.add_run('.')

    def _format_paragraph(self, paragraph):
        pass

    def _format_run(self, run, color=None, font='Times New Roman', font_size=Pt(14)):
        if type(color) == POS:
            run.font.color.rgb = color.value
        run.font.name = font
        run.font.size = font_size



if __name__ == '__main__':
    sheet = Worksheet(['In the summer, extreme temperatures of over 100 degrees can give visitors heat strokes.',
                       'Big Bend National Park is one of only two national parks in Texas.',
                       'The park looks totally different from the more populated eastern half of the state.'])
    sheet.render()
