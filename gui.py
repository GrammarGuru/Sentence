import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QPushButton, QDesktopWidget, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from worksheet import Worksheet


class Model(QMainWindow):
    def __init__(self, width=1000, height=800):
        super().__init__()
        self.width = width
        self.height = height
        self.initUI()


    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.statusBar().showMessage('Ready')
        
        self.add_btn = QPushButton('Add', self)
        self.add_btn.clicked.connect(self.add_line)
        self.add_btn.resize(self.add_btn.sizeHint())
        self.add_btn.move(0, 50)
        
        self.boxes = []
        for i in range(5):
            self.add_line()
        
        self.create_btn = QPushButton('Generate', self)
        self.create_btn.clicked.connect(self.generate)
        self.create_btn.resize(self.create_btn.sizeHint())
        self.create_btn.move(self.width - 100, self.height - 50)
        
        self.resize(self.width, self.height)
        self.setWindowTitle('Sentence')
        self.center()
        self.show()


    def add_line(self):
        box = QLineEdit(self)
        box.move(20, 50 * (len(self.boxes) + 1))
        box.resize(400, 40)
        self.boxes.append(box)
        self.add_btn.move(20, 50 * (len(self.boxes) + 1))
        box.show()


    def show_dialog(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText("Worksheet has been created.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()

    def generate(self):
        self.statusBar().showMessage('Generating documents')
        lines = self.get_data()
        questions = [line.replace(",", "") for line in lines]
        Worksheet(questions).render(key=False)
        Worksheet(lines).render(key=True)
        self.show_dialog()
        self.statusBar().showMessage('Ready')

    def get_data(self):
        lines = []
        for box in self.boxes:
            text = box.text()
            if len(text) != 0:
                lines.append(box.text())
        return lines

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Model()

    sys.exit(app.exec_())