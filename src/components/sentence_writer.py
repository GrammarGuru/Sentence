import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
from src.components.widget_utils import fill_layout, style_label
import requests

STYLE_LOC = 'config/style.json'
# Temporary! Remove when complete
URL = 'https://yourshot.nationalgeographic.com/u/fQYSUbVfts-T7odkrFJckdiFeHvab0GWOfzhj7tYdC0uglagsDNfPv0sS-NMmaDdqrBH7XJpEw-BSexevfhOP11ZfqrJwXvxE5smjSXI8ag9lhrcJjabSDM487_9iHTXZVijTF2BrXgkv3S5ZPsAZwOz4BPLHU5VxZ4btJHtEnx_WRbP7M0CPXEuZz7lwBaezXp82kZbs_47jOYnDGJ6XHhwjsLa/'
SENTENCE_FORMAT = [0, 1, 2, 3, 4, 5]


class SentenceWriter(QWidget):
    def __init__(self, url=URL, sentence_format=SENTENCE_FORMAT):
        super().__init__()
        self.setWindowTitle('Sentence Writer')
        self.layout = QVBoxLayout(self)
        img = self.get_image(url)
        instruction = get_instruction(sentence_format)
        textbox = self.get_textbox()

        fill_layout(self.layout, img, instruction, textbox)

    def get_textbox(self):
        return QTextEdit()

    def get_image(self, url):
        label = QLabel(self)
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(url).content)
        label.setPixmap(pixmap)
        return label

    def closeEvent(self, event):
        print(event)


def get_instruction(sentence_format):
    colors = get_colors()
    layout = QHBoxLayout()
    for tag in sentence_format:
        color = colors[tag]
        label = style_label(QLabel(color['name']), font_size=13, color=color['rgb'])
        layout.addWidget(label)

    return layout


def get_colors():
    with open(STYLE_LOC) as f:
        colors = json.load(f)
    result = [None] * len(colors)
    for color in colors.values():
        result[color['id']] = color
    return result


if __name__ == '__main__':
    STYLE_LOC = '../../config/style.json'
    app = QApplication(sys.argv)
    ex = SentenceWriter(URL, SENTENCE_FORMAT)
    ex.show()
    sys.exit(app.exec_())
