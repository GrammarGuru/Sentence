import sys
from .news_controller import NewsController
from PyQt5.QtWidgets import QWidget, \
    QPushButton, \
    QHBoxLayout, QApplication, QLayout
from PyQt5.QtGui import QFont


sheet = """
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
    btn.setStyleSheet(sheet)
    btn.setMinimumSize(120, 40)
    font = QFont()
    font.setPointSize(12)
    btn.setFont(font)
    return btn

def fill_layout(layout, *args):
    print(layout)
    for item in args:
        if isinstance(item, QLayout):
            layout.addLayout(item)
        else:
            layout.addWidget(item)

class Controller(QWidget):
    def __init__(self, generate_func, link_func, lines_func):
        super().__init__()
        self.init_layout()
        self.setStyleSheet(background_sheet)
        self.news_controller = NewsController(link_func, lines_func)
        news_btn = create_btn('News', self.show_news)
        generate_btn = create_btn('Generate', generate_func)
        fill_layout(self.layout, news_btn, generate_btn)
        
    def init_layout(self):
        self.layout = QHBoxLayout(self)
        self.layout.addStretch(1)

    def show_news(self):
        self.news_controller.show()


if __name__ == '__main__':
    f = lambda x: print("Button")
    app = QApplication(sys.argv)
    ex = Controller(f, f)
    ex.show()
    sys.exit(app.exec_())