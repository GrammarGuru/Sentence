import sys
from .news_controller import NewsController
from PyQt5.QtWidgets import QWidget, \
    QPushButton, \
    QHBoxLayout, QApplication


class Controller(QWidget):
    def __init__(self, generate_func, news_func):
        super().__init__()
        self.news_func = news_func

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addStretch(1)

        self.news_controller = NewsController(news_func)
        news_btn = QPushButton('News')
        news_btn.clicked.connect(self.show_news)
        self.layout.addWidget(news_btn)

        generate_btn = QPushButton('Generate')
        generate_btn.clicked.connect(generate_func)
        self.layout.addWidget(generate_btn)

    def show_news(self):
        self.news_controller.show()


if __name__ == '__main__':
    f = lambda x: print("Button")
    app = QApplication(sys.argv)
    ex = Controller(f, f)
    ex.show()
    sys.exit(app.exec_())