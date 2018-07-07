import os
from .worksheet import Worksheet
from src.api.news import crawl, break_paragraphs
from src.components.controller import Controller
from src.components.lines import Lines
from src.components.settings.pos_manager import PosManager
from src.components.settings.sheet_manager import SheetManager
from src.components.widget_utils import fill_layout, load_json
from PyQt5.QtWidgets import QMainWindow, \
    QToolTip, \
    QDesktopWidget, QHBoxLayout, \
    QMessageBox, QWidget, QVBoxLayout, \
    QFileDialog, QAction
from PyQt5.QtGui import QFont, QIcon

background_sheet = """
                    background-color: rgb(250, 250, 250)
                   """


class Model(QMainWindow):
    def __init__(self, data, width=1200, height=800):
        super().__init__()
        self.data = data
        self.setStyleSheet(background_sheet)
        self.width = width
        self.height = height
        self.settings = load_json('config/worksheet.json')
        self.initUI()
        self.format_window()

    def config_manager(self, manager, title):
        setting = QAction(title, self)
        setting.triggered.connect(lambda _: manager.show())
        return setting

    def add_toolbar(self):
        menu_bar = self.menuBar()

        color_action = self.config_manager(PosManager(), 'Edit POS')
        sheet_action = self.config_manager(SheetManager(), 'Worksheet Settings')

        format_menu = menu_bar.addMenu('Format')
        format_menu.addAction(color_action)
        format_menu.addAction(sheet_action)

    def set_layout(self):
        self.setCentralWidget(QWidget(self))
        self.layout = QHBoxLayout()
        self.centralWidget().setLayout(self.layout)

    def load_components(self):
        self.lines = Lines()
        self.controller = Controller(data=self.data,
                                     generate_func=self.generate,
                                     link_func=self.add_link,
                                     lines_func=self.add_lines)

    def format_window(self):
        self.resize(self.width, self.height)
        self.setWindowTitle('Sentence')
        self.setWindowIcon(QIcon('doc_icon.ico'))
        self.center()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.statusBar().showMessage('Ready')

        self.load_components()
        self.set_layout()
        self.add_toolbar()

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addWidget(self.controller)
        fill_layout(self.layout, self.lines, vbox)

    def add_link(self, link):
        self.lines.fill(crawl(link))

    def add_lines(self, lines):
        if self.settings['Paragraph Mode']:
            self.lines.fill(lines)
        else:
            self.lines.fill(break_paragraphs(lines))

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
                                               os.path.expanduser('~\\Documents'),
                                               'Microsoft Word Document (*.docx)')[0]
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


def get_title(loc):
    return loc[loc.rindex('/') + 1:loc.index('.')]
