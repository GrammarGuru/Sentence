import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QPushButton, QDesktopWidget, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from worksheet import Worksheet
from wikisheet import Wikisheet

class Box:
    def __init__(self, index, screen, height, remove_func):
        self.index = index
        self.box = QLineEdit(screen)
        self.box.move(20, height)
        self.box.resize(400, 40)
        
        self.close = QPushButton('X', screen)
        self.close.clicked.connect(lambda x: remove_func(self.index))
        self.close.resize(40, 40)
        self.close.move(430, height)
        
        self.box.show()
        self.close.show()
        
    def hide(self):
        self.box.setParent(None)
        self.close.setParent(None)
        
    def move(self, height):
        self.box.move(20, height)
        self.close.move(430, height)
    
    def text(self):
        return self.box.text()
    
    def setText(self, text):
        self.box.setText(text)
    
    def __str__(self):
        return str(self.index) + ' ' + self.box.text()
        
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
        self.create_btn.move(self.width - 150, self.height - 80)
        
        self.wiki_btn = QPushButton('Wikipedia', self)
        self.wiki_btn.clicked.connect(self.get_wiki)
        self.wiki_btn.resize(self.wiki_btn.sizeHint())
        self.wiki_btn.move(self.width - 260, self.height - 80)
        
        self.resize(self.width, self.height)
        self.setWindowTitle('Sentence')
        self.center()
        self.show()


    def add_line(self):
        index = len(self.boxes)
        self.boxes.append(Box(index, self, 50 * (index + 1), self.remove_line))
        self.add_btn.move(20, 50 * (len(self.boxes) + 1))
        
    def get_wiki(self):
        self.statusBar().showMessage('Grabbing sentences')
        sheet = Wikisheet()
        lines = sheet.get_lines(size=len(self.boxes))
        for i in range(len(lines)):
            if len(self.boxes[i].text()) == 0:
                self.boxes[i].setText(lines[i])
        self.show_dialog('Sentences generated')
        self.statusBar().showMessage('Ready')
        
    def remove_line(self, index):
        self.boxes[index].hide()
        del self.boxes[index]
        for i in range(index, len(self.boxes)):
            self.boxes[i].index = i
            self.boxes[i].move(50 * (i + 1))
            
        self.add_btn.move(20, 50 * (len(self.boxes) + 1))


    def show_dialog(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()

    def generate(self):
        self.statusBar().showMessage('Generating documents')
        lines = self.get_data()
        questions = [line.replace(",", "") for line in lines]
        try:
            Worksheet(questions).render(key=False)
            Worksheet(lines).render(key=True)
            self.show_dialog("Worksheet has been created.")
        except:
            self.show_dialog("Error: Make sure you close your word document before generating.")
        self.statusBar().showMessage('Ready')


    def get_data(self):
        lines = []
        for box in self.boxes:
            text = box.text()
            if len(text) != 0:
                lines.append(text)
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