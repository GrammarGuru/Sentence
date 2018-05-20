import sys
from PyQt5.QtWidgets import QWidget, \
    QTextEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QApplication, QScrollArea, QSizePolicy
from PyQt5.QtGui import QFont

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


        container = QWidget()
        container.setLayout(self.layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(False)
        scroll.setWidget(container)

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(scroll)

        add_btn = QPushButton('Add')
        add_btn.setStyleSheet(sheet)
        font = QFont()
        font.setPointSize(14)
        add_btn.setFont(font)
        add_btn.setMinimumHeight(40)
        add_btn.resize(add_btn.minimumSize())
        add_btn.clicked.connect(self.add_line)
        layout.addWidget(add_btn)

    def add_line(self):
        hbox = QHBoxLayout()
        box = QTextEdit()
        box.setStyleSheet(box_sheet)
        box.setMaximumHeight(100)
        box.setMinimumWidth(400)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        box.setSizePolicy(sizePolicy)
        self.lines.append(box)
        btn = QPushButton('X')
        btn.setStyleSheet(add_sheet)
        btn.setMaximumSize(40, 40)
        btn.setMinimumSize(35, 35)
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