import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFileDialog, QMessageBox
from src.widget_utils import fill_layout, style_btn
from src.api.nlp import get_sentences

class FileManager(QWidget):
    def __init__(self, lines_func):
        super().__init__()
        self.lines_func = lines_func
        self.layout = QVBoxLayout(self)

        self.input = QTextEdit()

        btn_layout = QHBoxLayout(self)
        btn_layout.addStretch(2)
        fill_layout(btn_layout,
                    create_btn('Choose File', self.load_file),
                    create_btn('Import', self.send_lines))

        fill_layout(self.layout, self.input, btn_layout)

    def load_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', os.path.expanduser('~\\Documents'))[0]
        print(filename)

    def send_lines(self):
        try:
            text = self.input.toPlainText().strip()
            if text:
                lines = get_sentences(self.input.toPlainText())
                self.lines_func(lines)
            self.close()
        except Exception as inst:
            print(inst)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('Error: Try Again')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.show()

    def show(self):
        self.resize(600, 600)
        super().show()


def create_btn(name, on_click):
    btn = QPushButton(name)
    style_btn(btn, 12, style='secondary')
    btn.setMinimumSize(80, 20)
    btn.clicked.connect(on_click)
    return btn