import sys
from src.components.news_controller.topic_controller import TopicController
from src.components.sentence_writer import SentenceWriter
from PyQt5.QtWidgets import QWidget, \
    QPushButton, \
    QHBoxLayout, QApplication
from PyQt5.QtGui import QFont
from .widget_utils import fill_layout


btn_sheet = """
        color: rgb(66, 184, 221);
        border-radius: 5px;
        border: 2px solid rgb(66, 184, 221);
        text-shadow 0 1px 1px rgba(0, 0, 0, 0.2);
        background-color: rgb(255, 255, 255);
        """
        
background_sheet = """
                    background-color: rgb(250, 250, 250)
                   """


def create_btn(name, on_click):
    btn = QPushButton(name)
    btn.clicked.connect(on_click)
    btn.setStyleSheet(btn_sheet)
    btn.setMinimumSize(120, 40)
    font = QFont()
    font.setPointSize(12)
    btn.setFont(font)
    return btn


class Controller(QWidget):
    def __init__(self, data, generate_func, link_func, lines_func):
        super().__init__()
        self.layout = self.init_layout()
        self.setStyleSheet(background_sheet)
        self.topic_controller = TopicController(data, link_func, lines_func)
        self.writer = SentenceWriter()

        write_btn = create_btn('Write', self.init_writer)
        news_btn = create_btn('News', self.show_news)
        generate_btn = create_btn('Generate', generate_func)

        fill_layout(self.layout, write_btn, news_btn, generate_btn)
        
    def init_layout(self):
        layout = QHBoxLayout(self)
        layout.addStretch(1)
        return layout

    def init_writer(self):
        try:
            self.writer.show()
        except Exception as inst:
            print(inst)

    def show_news(self):
        self.topic_controller.show()


if __name__ == '__main__':
    f = lambda x: print("Button")
    app = QApplication(sys.argv)
    ex = Controller(f, f)
    ex.show()
    sys.exit(app.exec_())