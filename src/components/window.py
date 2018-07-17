from PyQt5.QtWidgets import QWidget, QMainWindow

background_sheet = """
                    background-color: rgb(250, 250, 250)
                   """


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(background_sheet)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(background_sheet)
