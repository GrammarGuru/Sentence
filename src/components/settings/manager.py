import copy
import json

from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QLabel

from src.components.window import Window
from src.widget_utils import style_label


class Manager(Window):
    def __init__(self, loc, title='Manager', update_func=None):
        super().__init__()
        self.loc = loc
        self.update_func = update_func
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
        if self.update_func is not None:
            self.update_func()

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
