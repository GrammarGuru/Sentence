import sys
import json
from PyQt5.QtWidgets import QWidget, QHBoxLayout, \
    QVBoxLayout, QLabel, QPushButton, \
    QApplication, QColorDialog, QMessageBox
from PyQt5.QtGui import QFont
from .widget_utils import fill_layout, set_btn_font

sheet = """
        color: rgb(66, 184, 221);
        border-radius: 5px;
        border: 2px solid rgb(66, 184, 221);
        text-shadow 0 1px 1px rgba(0, 0, 0, 0.2);
        background-color: rgb(255, 255, 255);
        """

background_sheet = """
                    background-color: rgb(250, 250, 250)
                   """


class ColorManager(QWidget):
    def __init__(self, loc='config/style.json'):
        super().__init__()
        self.setStyleSheet(background_sheet)
        self.loc = loc
        self.styles = load_styles(loc)
        self.labels = {}
        self.change = False

        self.layout = QVBoxLayout(self)
        for name, style in self.styles.items():
            self.add_pos(name, style)

    def show(self):
        self.resize(400, 400)
        super().show()

    def add_pos(self, pos, style):
        layout = QHBoxLayout()
        color = style['rgb']
        name = style['name']

        label = self._create_label(name, color)
        btn = self._create_btn(pos)

        fill_layout(layout, label, btn)
        self.layout.addLayout(layout)

    def update(self, pos):
        color = parse_rgb(QColorDialog.getColor().rgb())
        if color != [0, 0, 0]:
            self.change = True
            self.styles[pos]['rgb'] = color
            self.update_color(pos, color)

    def update_color(self, name, color):
        label = self.labels[name]
        set_color(label, color)

    def closeEvent(self, event):
        print("Close Event")
        if self.change:
            reply = QMessageBox.question(self, 'Save changes', "Would you like to save changes?", QMessageBox.Yes,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.save_state()
            else:
                self.reset()

    def save_state(self):
        with open(self.loc, 'w') as f:
            f.write(json.dumps(self.styles))

    def reset(self):
        self.styles = load_styles(self.loc)
        for name, style in self.styles.items():
            print(name, style['rgb'])
            self.update_color(name, style['rgb'])
        self.change = False

    def _create_btn(self, id):
        btn = QPushButton('Edit')
        btn.setStyleSheet(sheet)
        set_btn_font(btn, 13)
        btn.setMinimumSize(80, 40)
        btn.clicked.connect(lambda _, pos_id=id: self.update(pos_id))
        return btn

    def _create_label(self, name, color):
        label = QLabel(name)
        self.labels[name] = label
        set_color(label, color)
        label.setFont(QFont('Times New Roman', 13))
        return label


def set_color(label, color):
    label.setStyleSheet("""
                        color: {}
                        """.format(format_rgb(color)))


def load_styles(loc):
    with open(loc) as f:
        return json.load(f)


def format_rgb(rgb):
    return 'rgb({},{},{})'.format(*rgb)


def parse_rgb(rgb):
    return [(rgb >> num) & 0xFF for num in range(16, -1, -8)]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ColorManager(loc='../../style.json')
    ex.show()
    sys.exit(app.exec_())
