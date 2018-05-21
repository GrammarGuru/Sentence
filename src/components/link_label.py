from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
import webbrowser


class LinkLabel(QLabel):
    def __init__(self, text, link, font_size=12):
        super().__init__(text)
        self.link = link
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)

    def mousePressEvent(self, event):
        webbrowser.open(self.link)