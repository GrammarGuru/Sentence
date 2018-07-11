from PyQt5.QtWidgets import QHBoxLayout, \
    QLabel, QPushButton, \
    QColorDialog, QCheckBox
from ..widget_utils import fill_layout, style_btn, style_label, set_color
from .manager import Manager

sheet = """
        color: rgb(66, 184, 221);
        border-radius: 5px;
        border: 2px solid rgb(66, 184, 221);
        text-shadow 0 1px 1px rgba(0, 0, 0, 0.2);
        background-color: rgb(255, 255, 255);
        """


class PosManager(Manager):
    def __init__(self, loc='config/pos.json', title='Part of Speech Settings'):
        super().__init__(loc, title)
        self.labels = {}

        settings = [self.create_setting(name, style) for name, style in self.settings.items()]
        fill_layout(self.layout, *settings)

    def show(self):
        self.resize(600, 400)
        super().show()

    def create_setting(self, pos, style):
        layout = QHBoxLayout()
        color = style['rgb']
        name = style['name']
        active = style['active']

        self.labels[pos] = self._create_label(name, color)
        btn = self._create_btn(pos)
        checkbox = QCheckBox("Activate")
        checkbox.setChecked(active)
        checkbox.stateChanged.connect(lambda _, p=pos: self.update_status(p))

        fill_layout(layout, self.labels[pos], btn, checkbox)
        return layout

    def update_color(self, pos):
        color = QColorDialog.getColor()
        if color.isValid():
            rgb = parse_rgb(color.rgb())
            self.settings[pos]['rgb'] = rgb
            set_color(self.labels[pos], rgb)

    def update_status(self, pos):
        self.settings[pos]['active'] = not self.settings[pos]['active']

    def _create_btn(self, id):
        btn = QPushButton('Edit Color')
        btn.setStyleSheet(sheet)
        style_btn(btn, 13)
        btn.setMinimumSize(80, 40)
        btn.clicked.connect(lambda _, pos_id=id: self.update_color(pos_id))
        return btn

    @staticmethod
    def _create_label(name, color):
        label = QLabel(name)
        style_label(label, font_size=13, color=color)
        return label


def parse_rgb(rgb):
    return [(rgb >> num) & 0xFF for num in range(16, -1, -8)]
