import sys
from PyQt5.QtWidgets import QWidget, \
    QTextEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QApplication, QScrollArea, QSizePolicy
from PyQt5.QtGui import QFont
from .widget_utils import fill_layout

sheet = """
        color: rgb(66, 184, 221);
        border-radius: 5px;
        border: 2px solid rgb(66, 184, 221);
        text-shadow 0 1px 1px rgba(0, 0, 0, 0.2);
        background-color: rgb(255, 255, 255);
        """

add_sheet = """
            color: rgb(232, 93, 117);
            border-radius: 5px;
            border: 2px solid rgb(232, 93, 117);
            text-shadow 0 1px 1px rgba(0, 0, 0, 0.2);
            background-color: rgb(255, 255, 255);
            """

background_sheet = """
                    background-color: rgb(250, 250, 250)
                   """

box_sheet = """
            background-color: white;
            """


class Lines(QWidget):
    def __init__(self):
        super().__init__()
        self.size = 0
        self.setStyleSheet(background_sheet)
        self.layout = QVBoxLayout()
        self.lines = []

        for i in range(10):
            self.add_line()

        layout = self.get_layout()

        add_btn = self.create_add_btn()
        layout.addWidget(add_btn)

    def create_add_btn(self):
        btn = QPushButton('Add')
        btn.setStyleSheet(sheet)
        font = QFont()
        font.setPointSize(14)
        btn.setFont(font)
        btn.setMinimumHeight(40)
        btn.resize(btn.minimumSize())
        btn.clicked.connect(self.add_line)
        return btn

    def get_layout(self):
        container = QWidget()
        container.setLayout(self.layout)
        scroll = create_scroll_area(container)

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(scroll)
        return layout

    def add_line(self):
        hbox = QHBoxLayout()

        box = create_text_box()
        self.lines.append(box)
        btn = create_remove_btn()
        btn.clicked.connect(lambda x: self.remove_line(hbox, box, btn))

        index = self.size
        fill_layout(hbox, box, btn)
        self.layout.insertLayout(index, hbox)
        self.size += 1

    def fill(self, lines):
        index = 0
        for line in self.lines:
            if index == len(lines):
                return
            if not line.toPlainText():
                line.setText(lines[index])
                index += 1

    def remove_line(self, line, box, btn):
        box.deleteLater()
        btn.deleteLater()
        line.deleteLater()
        del self.lines[self.lines.index(box)]
        self.size -= 1

    def get_data(self):
        result = []
        for line in self.lines:
            text = line.toPlainText()
            if text:
                result.append(text)
        return result


def create_scroll_area(container):
    scroll = QScrollArea()
    scroll.setWidgetResizable(False)
    scroll.setWidget(container)
    return scroll


def create_text_box():
    box = QTextEdit()
    box.setStyleSheet(box_sheet)
    box.setMaximumHeight(100)
    box.setMinimumWidth(420)
    sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    box.setSizePolicy(sizePolicy)
    return box


def create_remove_btn():
    btn = QPushButton('X')
    btn.setStyleSheet(add_sheet)
    btn.setMaximumSize(40, 40)
    btn.setMinimumSize(35, 35)
    return btn


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Lines()
    ex.show()
    sys.exit(app.exec_())
