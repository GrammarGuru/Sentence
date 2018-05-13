from PyQt5.QtWidgets import QWidget, QLabel
import webbrowser


class LinkLabel(QLabel):
    def __init__(self, text, link):
        super().__init__(text)
        self.link = link

    def mousePressEvent(self, event):
        webbrowser.open(self.link)