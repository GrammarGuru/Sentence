import sys
from .worksheet import Worksheet
from .newscrawler import crawl
from src.components.controller import Controller
from src.components.lines import Lines
from src.components.color_manager import ColorManager
from PyQt5.QtWidgets import QMainWindow, \
    QToolTip, \
    QDesktopWidget, QHBoxLayout, \
    QMessageBox, QWidget, QVBoxLayout, \
    QFileDialog, QAction
from PyQt5.QtGui import QFont


def get_title(loc):
    return loc[loc.rindex('/') + 1:loc.index('.')]


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
        
        color_manager = ColorManager()
        menu_bar = self.menuBar()
        format_menu = menu_bar.addMenu('Format')
        change_color = QAction('Edit Colors', self)
        change_color.triggered.connect(lambda _: color_manager.show())
        format_menu.addAction(change_color)

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

    @property
    def get_filename(self):
        try:
            return QFileDialog.getSaveFileName(self, 'Save Worksheet',
                                           'C:\\', 'Microsoft Word Document (*.docx)')[0]
        except:
            self.show_dialog("Error: Invalid File Name")

    def generate(self):
        file_loc = self.get_filename
        if file_loc is None:
            return
        title = get_title(file_loc)
        self.statusBar().showMessage('Generating documents')
        lines = self.lines.get_data()
        questions = [line.replace(",", "") for line in lines]
        try:
            Worksheet(questions, title=title, loc=file_loc, key=False).render()
            Worksheet(lines, title=title, loc=file_loc, key=True).render()
            self.show_dialog("Worksheet has been created.")
        except Exception as inst:
            print(inst)
            self.show_dialog("Error: Make sure you close your word document before generating.")
        self.statusBar().showMessage('Ready')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())