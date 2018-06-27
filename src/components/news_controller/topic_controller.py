import sys
from PyQt5.QtWidgets import QWidget, \
    QPushButton, QGridLayout, QVBoxLayout, \
    QHBoxLayout, QLabel, QLineEdit, QMessageBox, \
    QApplication
from PyQt5.QtGui import QFont
from src.components.widget_utils import fill_layout
from src.components.news_controller.news_controller import NewsController

background_sheet = """
                    background-color: rgb(250, 250, 250)
                   """

btn_sheet = """
        color: rgb(255, 255, 255);
        border-radius: 5px;
        border: 2px solid rgb(66, 184, 221);
        text-shadow 0 1px 1px rgba(0, 0, 0, 0.2);
        background-color: rgb(66, 184, 221);
        """

header_sheet = """
                color: rgb(66, 184, 221);
               """


def create_label(name):
    label = QLabel(name)
    label.setStyleSheet(header_sheet)
    label.setFont(QFont('Times New Roman', 13))
    return label


def create_btn(name, on_click, large=True):
    btn = QPushButton(name)
    btn.setStyleSheet(btn_sheet)
    btn.clicked.connect(on_click)
    if large:
        btn.setMinimumSize(150, 50)
    font = QFont()
    font.setPointSize(12)
    btn.setFont(font)
    return btn


class TopicController(QWidget):
    def __init__(self, data, link_func, lines_func):
        super().__init__()
        self.setStyleSheet(background_sheet)
        self.data = data
        self.link_func = link_func
        self.lines_func = lines_func
        self.layout = QVBoxLayout(self)

        manual_layout = self.add_link_input()
        grid = self.add_topics()

        fill_layout(self.layout, manual_layout, grid)

    def add_link_input(self):
        manual_label = create_label('Enter Link')
        manual_layout = QHBoxLayout()
        manual_line = QLineEdit()
        manual_btn = create_btn('Add', lambda: self.send_link(manual_line.text()), large=False)
        fill_layout(manual_layout, manual_label, manual_line, manual_btn)
        return  manual_layout

    def add_topics(self):
        grid = QGridLayout()
        grid.setSpacing(20)
        index = 0
        for topic, articles in self.data.items():
            topic = topic.capitalize()
            on_click = lambda _, t=topic, a=articles: self.load_topic(t, a)
            btn = create_btn(topic, on_click)
            grid.addWidget(btn, index // 2, index % 2)
            index += 1

        return grid

    def send_link(self, link):
        try:
            self.link_func(link)
        except Exception as inst:
            print(inst)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('Error: Check Link and Try Again')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.show()

    def load_topic(self, topic, articles):
        try:
            NewsController(topic, articles, self.lines_func).show()
        except Exception as inst:
            print(inst)


if __name__ == '__main__':
    test_data = {
        'world': [],
        'life': [],
        'tech': [],
        'money': [],
        'business': [],
        'travel': []
    }
    func = lambda: print("asdf")
    app = QApplication(sys.argv)
    ex = TopicController(test_data, func, func)
    ex.show()
    sys.exit(app.exec_())
