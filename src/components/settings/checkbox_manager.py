from PyQt5.QtWidgets import \
    QCheckBox

from src.widget_utils import fill_layout
from .manager import Manager

background_sheet = """
                    background-color: rgb(250, 250, 250)
                   """


class CheckboxManager(Manager):
    def __init__(self, loc, title='Worksheet Settings', update_func=None):
        super().__init__(loc, title, update_func)
        settings = [self.create_setting(name, active) for name, active in self.settings.items()]
        fill_layout(self.layout, *settings)

    def create_setting(self, name, active):
        checkbox = QCheckBox(name)
        checkbox.setChecked(active)
        checkbox.stateChanged.connect(lambda _, n=name: self.update_status(n))
        return checkbox

    def show(self):
        self.resize(200, 200)
        super().show()

    def update_status(self, setting):
        self.settings[setting] = not self.settings[setting]
