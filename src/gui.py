import os
import random

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, \
    QToolTip, \
    QDesktopWidget, QHBoxLayout, \
    QWidget, QVBoxLayout, \
    QFileDialog, QAction

from services.worksheet import create_worksheet
from src.api.news import crawl, break_paragraphs
from src.api.nlp import filter_lines
from src.components.controller import Controller
from src.components.lines import Lines
from src.components.settings.checkbox_manager import CheckboxManager
from src.components.settings.pos_manager import PosManager
from src.widget_utils import fill_layout, load_json, show_dialog

background_sheet = """
                    background-color: rgb(250, 250, 250)
                   """

WORKSHEET_SETTINGS = 'config/worksheet.json'
WEB_SETTINGS = 'config/web.json'


class Model(QMainWindow):
    def __init__(self, data, width=1200, height=800):
        super().__init__()
        self.data = data
        self.sources = []
        self.setStyleSheet(background_sheet)
        self.width = width
        self.height = height
        self.load_settings()
        self.initUI()
        self.format_window()

    def config_manager(self, manager, title):
        setting = QAction(title, self)
        setting.triggered.connect(lambda _: manager.show())
        return setting

    def add_toolbar(self):
        menu_bar = self.menuBar()

        color_action = self.config_manager(PosManager(), 'Edit POS')
        sheet_action = self.config_manager(CheckboxManager(loc=WORKSHEET_SETTINGS,
                                                           title='Worksheet Settings',
                                                           update_func=self.load_settings),
                                           'Worksheet Settings')
        web_actions = self.config_manager(CheckboxManager(loc=WEB_SETTINGS,
                                                          title='Web Settings',
                                                          update_func=self.load_settings),
                                          'Web Settings')

        format_menu = menu_bar.addMenu('Format')
        format_menu.addAction(color_action)
        format_menu.addAction(sheet_action)
        format_menu.addAction(web_actions)

    def set_layout(self):
        self.setCentralWidget(QWidget(self))
        self.layout = QHBoxLayout()
        self.centralWidget().setLayout(self.layout)

    def load_components(self):
        self.lines = Lines(reset_func=self.reset)
        self.controller = Controller(data=self.data,
                                     generate_func=self.generate,
                                     link_func=self.add_link,
                                     lines_func=self.add_lines)

    def load_settings(self):
        self.settings = {**load_json(WORKSHEET_SETTINGS), **load_json(WEB_SETTINGS)}

    def format_window(self):
        self.resize(self.width, self.height)
        self.setWindowTitle('Sentence')
        self.setWindowIcon(QIcon('assets/doc_icon.ico'))
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
        self.add_lines(crawl(link), link)

    def reset(self):
        self.sources = []

    def add_lines(self, lines, link=None):
        if link is not None and self.settings['Include Sources']:
            self.sources.append(link)
        if not self.settings['Paragraph Mode']:
            lines = break_paragraphs(lines)
        if self.settings['Randomize']:
            random.shuffle(lines)
        self.lines.fill(filter_lines(lines))

    @property
    def get_filename(self):
        return QFileDialog.getSaveFileName(self, 'Save Worksheet',
                                           os.path.expanduser('~\\Documents'),
                                           'Microsoft Word Document (*.docx)')[0]

    def generate(self):
        self.statusBar().showMessage('Generating documents')
        file_loc = self.get_filename
        if len(file_loc) == 0:
            return
        title = get_title(file_loc)
        sources = self.sources if self.settings['Include Sources'] else []
        lines = self.lines.get_data()
        if len(lines) == 0:
            show_dialog(self, "Error: Make sure to add some sentences.")
            return
        try:
            create_worksheet(file_loc, title, lines, sources, self.settings)
            show_dialog(self, "Worksheet has been created.")
        except Exception as inst:
            print(inst)
            show_dialog(self, "Error: Make sure you close your word document before generating.")
        self.statusBar().showMessage('Ready')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def get_title(loc):
    start = loc.rindex('/') + 1
    end = loc.index('.')
    return loc[start:end]
