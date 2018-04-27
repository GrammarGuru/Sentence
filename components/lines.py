import sys
from PyQt5.QtWidgets import QWidget, \
    QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QApplication


class Lines(QWidget):
    def __init__(self):
        super().__init__()
        self.size = 0
        self.unfilled = 0
        self.layout = QVBoxLayout()
        self.lines = []

        for i in range(5):
            self.add_line()

        add_btn = QPushButton('Add')
        add_btn.clicked.connect(self.add_line)
        self.layout.addWidget(add_btn)

        self.setLayout(self.layout)
        self.show()

    def add_line(self):
        hbox = QHBoxLayout()
        box = QLineEdit()
        self.lines.append(box)
        btn = QPushButton('X')
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
            if not line.text():
                line.setText(lines[index])
                index += 1

    def remove_line(self, line, box, btn):
        box.deleteLater()
        btn.deleteLater()
        line.deleteLater()
        self.size -= 1

    def get_data(self):
        result = []
        for line in self.lines:
            text = line.text()
            if text:
                result.append(result)
        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Lines()
    sys.exit(app.exec_())