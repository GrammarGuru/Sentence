import sys
import json
from PyQt5.QtWidgets import QWidget, QHBoxLayout, \
QVBoxLayout, QLabel, QPushButton, \
QApplication, QColorDialog, QMessageBox, QLayout
from .widget_utils import fill_layout


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

def load_styles(loc):
    with open(loc) as f:
        return json.load(f)
    
def format_rgb(rgb):
    return 'rgb({},{},{})'.format(*rgb)

def parse_rgb(rgb):
    return [(rgb >> num) & 0xFF for num in range(16, -1, -8)]

    
class ColorManager(QWidget):
    def __init__(self, loc='config/style.json'):
        super().__init__()
        self.setStyleSheet(background_sheet)
        self.loc = loc
        self.styles = load_styles(loc)
        self.labels = {}
        self.change = False
        
        self.layout = QVBoxLayout(self)
        for name, style in self.styles.items():
            self.add_pos(name, style['rgb'])
    
    def add_pos(self, name, color):
        layout = QHBoxLayout()
        
        label = QLabel(name)
        self.labels[name] = label
        self.update_color(name, color)

        btn = QPushButton('Edit')
        btn.setStyleSheet(sheet)
        btn.clicked.connect(lambda _, pos=name: self.update(pos))
        
        fill_layout(layout, label, btn)
        self.layout.addLayout(layout)
        
    def update(self, pos):
        color = parse_rgb(QColorDialog.getColor().rgb())
        if color != [0, 0, 0]:
            self.change = True
            self.styles[pos]['rgb'] = color
            self.update_color(pos, color)
        
    def update_color(self, name, color):
        label = self.labels[name]
        label.setStyleSheet("""
                           color: {}
                           """.format(format_rgb(color)))
    def save_state(self):
        with open(self.loc, 'w') as f:
            f.write(json.dumps(self.styles))
            
    def closeEvent(self, event):
        print("Close Event")
        if self.change:
            reply = QMessageBox.question(self, 'Save changes', "Would you like to save changes?", QMessageBox.Yes, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.save_state()
        
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ColorManager(loc='../../style.json')
    ex.show()
    sys.exit(app.exec_())