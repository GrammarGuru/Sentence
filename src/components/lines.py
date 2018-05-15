import sys
from PyQt5.QtWidgets import QWidget, \
    QTextEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QApplication, QScrollArea


class Lines(QWidget):
    def __init__(self):
        super().__init__()
        self.size = 0
        self.layout = QVBoxLayout()
        self.lines = []

        for i in range(10):
            self.add_line()


        container = QWidget()
        container.setLayout(self.layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(False)
        scroll.setWidget(container)

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(scroll)

        add_btn = QPushButton('Add')
        add_btn.resize(add_btn.minimumSize())
        add_btn.clicked.connect(self.add_line)
        layout.addWidget(add_btn)

    def add_line(self):
        hbox = QHBoxLayout()
        box = QTextEdit()
        box.setMaximumHeight(100)
        box.setMinimumWidth(400)
        self.lines.append(box)
        btn = QPushButton('X')
        btn.setMaximumSize(30, 30)
        btn.clicked.connect(lambda x: self.remove_line(hbox, box, btn))
        index = self.size

        hbox.addWidget(box)
        hbox.addWidget(btn)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Lines()
    ex.show()
    sys.exit(app.exec_())