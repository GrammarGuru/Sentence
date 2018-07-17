import json

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLayout, QMessageBox, QPushButton, QLabel

primary_btn_sheet = """
        color: rgb(66, 184, 221);
        border-radius: 5px;
        border: 2px solid rgb(66, 184, 221);
        text-shadow 0 1px 1px rgba(0, 0, 0, 0.2);
        background-color: rgb(255, 255, 255);
        """

secondary_btn_sheet = """
        color: rgb(255, 255, 255);
        border-radius: 5px;
        border: 2px solid rgb(66, 184, 221);
        text-shadow 0 1px 1px rgba(0, 0, 0, 0.2);
        background-color: rgb(66, 184, 221);
        """

warning_btn_sheet = """
            color: rgb(232, 93, 117);
            border-radius: 5px;
            border: 2px solid rgb(232, 93, 117);
            text-shadow 0 1px 1px rgba(0, 0, 0, 0.2);
            background-color: rgb(255, 255, 255);
            """

header_label_sheet = """
            color: rgb(66, 184, 221);
             """


def fill_layout(layout, *args):
    for item in args:
        if isinstance(item, QLayout):
            layout.addLayout(item)
        else:
            layout.addWidget(item)


def create_btn(name, on_click, font_size=12, style='primary', size=None):
    btn = QPushButton(name)
    btn.clicked.connect(on_click)
    style_btn(btn, font_size, style, size)
    return btn


def style_btn(btn, font_size, style='primary', size=None):
    if style == 'primary':
        btn.setStyleSheet(primary_btn_sheet)
    elif style == 'secondary':
        btn.setStyleSheet(secondary_btn_sheet)
    elif style == 'warning':
        btn.setStyleSheet(warning_btn_sheet)
    else:
        raise ValueError()
    font = QFont('Times New Roman', font_size)
    btn.setFont(font)
    if size is not None:
        btn.setMinimumSize(*size)
    return btn


def create_label(text, font_size=13, color=(0, 0, 0), style=None):
    return style_label(QLabel(text), font_size, color, style)


def style_label(label, font_size, color=(0, 0, 0), style=None):
    font = QFont('Times New Roman', font_size)
    label.setFont(font)
    if style is not None:
        label.setStyleSheet(header_label_sheet)
    if color != (0, 0, 0):
        set_color(label, color)
    return label


def show_dialog(self, message):
    msg = QMessageBox(self)
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.show()


def set_color(label, color):
    label.setStyleSheet("""
                        color: {}
                        """.format(format_rgb(color)))
    return label


def format_rgb(rgb):
    return 'rgb({},{},{})'.format(*rgb)


def load_json(loc):
    with open(loc) as f:
        return json.load(f)

