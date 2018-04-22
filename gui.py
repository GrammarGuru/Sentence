import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QPushButton, QDesktopWidget, QLineEdit
from PyQt5.QtGui import QFont


class Example(QMainWindow):
    def __init__(self, width=1000, height=800):
        super().__init__()
        self.width = width
        self.height = height
        self.initUI()


    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')
        self.statusBar().showMessage('Ready')

        self.add_btn = QPushButton('Add', self)
        self.add_btn.clicked.connect(lambda x: self.add_line(show=True))
        self.add_btn.resize(self.add_btn.sizeHint())
        self.add_btn.move(0, 50)

        self.boxes = []
        for i in range(5):
            self.add_line(show=False)

        self.create_btn = QPushButton('Generate', self)
        self.create_btn.clicked.connect(QApplication.instance().quit)
        self.create_btn.setToolTip('This is a <b>QPushButton</b> widget')
        self.create_btn.resize(self.create_btn.sizeHint())
        self.create_btn.move(self.width - 100, self.height - 50)

        self.resize(self.width, self.height)
        self.setWindowTitle('Sentence')
        self.center()
        self.show()


    def add_line(self, show=True):
        box = QLineEdit(self)
        box.move(20, 50 * (len(self.boxes) + 1))
        box.resize(400, 40)
        self.boxes.append(box)
        self.add_btn.move(20, 50 * (len(self.boxes) + 1))

        print(show)
        if show:
            self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())