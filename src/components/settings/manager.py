from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QLabel
import json
import copy
from ..widget_utils import style_label

background_sheet = """
                    background-color: rgb(250, 250, 250)
                   """


class Manager(QWidget):
    def __init__(self, loc, title='Manager'):
        super().__init__()
        self.loc = loc
        self.setStyleSheet(background_sheet)
        self.settings = load(loc)
        self.initSettings = copy.deepcopy(self.settings)
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.create_title(title))
    
    def closeEvent(self, event):
        if self.settings != self.initSettings:
            reply = QMessageBox.question(self, 'Save changes',
                                         "Would you like to save changes?",
                                         QMessageBox.Yes,
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.save_state()
            else:
                self.reset()

    def save_state(self):
        with open(self.loc, 'w') as f:
            f.write(json.dumps(self.settings))

    def reset(self):
        self.settings = self.initSettings
        self.initSettings = copy.deepcopy(self.settings)

    @staticmethod
    def create_title(title):
        label = QLabel(title)
        style_label(label, 16)
        return label
        

def load(loc):
    with open(loc) as f:
        return json.load(f)
