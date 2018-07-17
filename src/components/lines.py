import sys

from PyQt5.QtWidgets import QWidget, \
    QTextEdit, QVBoxLayout, \
    QHBoxLayout, QApplication, QScrollArea

from src.components.window import Window
from src.widget_utils import fill_layout, create_btn


class Lines(Window):
    def __init__(self, reset_func=None):
        super().__init__()
        self.size = 0
        self.reset_func = reset_func
        self.layout = QVBoxLayout()
        self.lines = []

        for i in range(10):
            self.add_line()

        layout = self.get_layout()

        add_btn = create_control_btn('Add', self.add_line)
        clear_btn = create_control_btn('Reset', self.reset)
        fill_layout(layout, add_btn, clear_btn)

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
        btn = create_remove_btn(lambda: self.remove_line(hbox, box, btn))

        index = self.size
        fill_layout(hbox, box, btn)
        self.layout.insertLayout(index, hbox)
        self.size += 1

    def reset(self):
        for line in self.lines:
            line.setText('')
        if self.reset_func is not None:
            self.reset_func()

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
    box.setMaximumHeight(100)
    box.setMinimumWidth(420)
    return box


def create_remove_btn(on_click):
    return create_btn('X', on_click, style='warning', size=(40, 40))


def create_control_btn(title, on_click):
    btn = create_btn(title, on_click)
    btn.setMinimumHeight(40)
    btn.resize(btn.minimumSize())
    return btn


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Lines()
    ex.show()
    sys.exit(app.exec_())
