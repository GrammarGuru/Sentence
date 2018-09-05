from PyQt5.QtWidgets import QLabel
import webbrowser
from src.widget_utils import style_label


class LinkLabel(QLabel):
    def __init__(self, text, link, font_size=12):
        super().__init__(text)
        self.link = link
        style_label(self, font_size)

    def mousePressEvent(self, event):
        webbrowser.open(self.link)
