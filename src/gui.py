import sys
from .worksheet import Worksheet
from .newscrawler import crawl
from src.components.controller import Controller
from src.components.lines import Lines
from PyQt5.QtWidgets import QMainWindow, \
    QToolTip, \
    QDesktopWidget, QHBoxLayout, \
    QMessageBox, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont

        
class Model(QMainWindow):
    def __init__(self, width=1000, height=800):
        super().__init__()
        self.width = width
        self.height = height
        self.initUI()


    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.statusBar().showMessage('Ready')

        self.lines = Lines()
        self.controller = Controller(generate_func=self.generate, news_func=self.add_news)

        self.setCentralWidget(QWidget(self))
        self.layout = QHBoxLayout()
        self.centralWidget().setLayout(self.layout)

        self.layout.addWidget(self.lines)
        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addWidget(self.controller)
        self.layout.addLayout(vbox)

        self.resize(self.width, self.height)
        self.setWindowTitle('Sentence')
        self.center()
        self.show()


    def add_news(self, link):
        self.lines.fill(crawl(link))

    def show_dialog(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()

    def generate(self):
        self.statusBar().showMessage('Generating documents')
        lines = self.lines.get_data()
        for line in lines:
            print(type(line), line)
        questions = [line.replace(",", "") for line in lines]
        try:
            Worksheet(questions).render(key=False)
            Worksheet(lines).render(key=True)
            self.show_dialog("Worksheet has been created.")
        except:
            self.show_dialog("Error: Make sure you close your word document before generating.")
        self.statusBar().showMessage('Ready')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())