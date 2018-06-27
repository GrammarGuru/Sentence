from PyQt5.QtWidgets import QLayout
from PyQt5.QtGui import QFont


def fill_layout(layout, *args):
    for item in args:
        if isinstance(item, QLayout):
            layout.addLayout(item)
        else:
            layout.addWidget(item)


def set_btn_font(btn, font_size, style='Times New Roman'):
    font = QFont(style, font_size)
    btn.setFont(font)
