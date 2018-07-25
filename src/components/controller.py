import sys

from PyQt5.QtWidgets import \
    QHBoxLayout, QApplication

from src.components.file_manager import FileManager
from src.components.news_controller.topic_controller import TopicController
from src.components.window import Window
from src.widget_utils import fill_layout, create_btn


class Controller(Window):
    def __init__(self, news_data, web_data, generate_func, link_func, lines_func):
        super().__init__()
        self.lines_func = lines_func
        self.layout = self.init_layout()
        self.topic_controller = TopicController(news_data, link_func, lines_func)
        self.web_controller = TopicController(web_data, link_func, lines_func, manual=False)

        fill_layout(self.layout,
                    create('Import', self.show_file_manager),
                    create('Web', self.show_web),
                    create('News', self.show_news),
                    create('Generate', generate_func))
        
    def init_layout(self):
        layout = QHBoxLayout(self)
        layout.addStretch(1)
        return layout

    def show_news(self):
        self.topic_controller.show()

    def show_web(self):
        self.web_controller.show()

    def show_file_manager(self):
        self.file_manager = FileManager(self.lines_func)
        self.file_manager.show()


def create(name, on_click):
    return create_btn(name, on_click, font_size=12, style='primary', size=(120, 40))


if __name__ == '__main__':
    f = lambda x: print("Button")
    app = QApplication(sys.argv)
    ex = Controller(f, f)
    ex.show()
    sys.exit(app.exec_())