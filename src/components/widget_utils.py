from PyQt5.QtWidgets import QLayout
from PyQt5.QtGui import QFont


def fill_layout(layout, *args):
    for item in args:
        if isinstance(item, QLayout):
            layout.addLayout(item)
        else:
            layout.addWidget(item)


def style_btn(btn, font_size, style='Times New Roman'):
    font = QFont(style, font_size)
    btn.setFont(font)
    return btn


def style_label(label, font_size, color, style='Times New Roman'):
    font = QFont(style, font_size)
    label.setFont(font)
    set_color(label, color)
    return label


def set_color(label, color):
    label.setStyleSheet("""
                        color: {}
                        """.format(format_rgb(color)))
    return label


def format_rgb(rgb):
    return 'rgb({},{},{})'.format(*rgb)

