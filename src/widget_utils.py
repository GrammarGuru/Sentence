from PyQt5.QtWidgets import QLayout, QMessageBox
from PyQt5.QtGui import QFont
import json

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


def fill_layout(layout, *args):
    for item in args:
        if isinstance(item, QLayout):
            layout.addLayout(item)
        else:
            layout.addWidget(item)


def style_btn(btn, font_size, style='primary'):
    if style == 'primary':
        btn.setStyleSheet(primary_btn_sheet)
    elif style == 'secondary':
        btn.setStyleSheet(secondary_btn_sheet)
    else:
        raise ValueError()
    font = QFont('Times New Roman', font_size)
    btn.setFont(font)
    return btn


def style_label(label, font_size, color=(0, 0, 0), style='Times New Roman'):
    font = QFont(style, font_size)
    label.setFont(font)
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

