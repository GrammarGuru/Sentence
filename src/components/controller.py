import sys
from .news_controller import NewsController
from PyQt5.QtWidgets import QWidget, \
    QPushButton, \
    QHBoxLayout, QApplication
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


class Controller(QWidget):
    def __init__(self, generate_func, link_func, lines_func):
        super().__init__()
        self.setStyleSheet(background_sheet)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addStretch(1)

        self.news_controller = NewsController(link_func, lines_func)
        news_btn = QPushButton('News')
        news_btn.clicked.connect(self.show_news)
        news_btn.setStyleSheet(sheet)
        news_btn.setMinimumSize(120, 40)
        font = QFont()
        font.setPointSize(12)
        news_btn.setFont(font)
        self.layout.addWidget(news_btn)
        
        generate_btn = QPushButton('Generate')
        generate_btn.setStyleSheet(sheet)
        generate_btn.clicked.connect(generate_func)
        generate_btn.setMinimumSize(120, 40)
        font = QFont()
        font.setPointSize(12)
        generate_btn.setFont(font)
        self.layout.addWidget(generate_btn)

    def show_news(self):
        self.news_controller.show()


if __name__ == '__main__':
    f = lambda x: print("Button")
    app = QApplication(sys.argv)
    ex = Controller(f, f)
    ex.show()
    sys.exit(app.exec_())