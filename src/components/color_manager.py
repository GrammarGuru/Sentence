import sys
import json
from PyQt5.QtWidgets import QWidget, QHBoxLayout, \
QVBoxLayout, QLabel, QPushButton, QApplication, QColorDialog


def load_styles(loc):
    with open(loc) as f:
        return json.load(f)
    
def format_rgb(rgb):
    return 'rgb({},{},{})'.format(*rgb)

def parse_rgb(rgb):
    return [(rgb >> num) & 0xFF for num in range(16, -1, -8)]
    
class ColorManager(QWidget):
    def __init__(self, loc='style.json'):
        super().__init__()
        self.loc = loc
        self.styles = load_styles(loc)
        self.labels = {}
        
        self.layout = QVBoxLayout(self)
        for name, style in self.styles.items():
            self.add_pos(name, style['rgb'])
    
    def add_pos(self, name, color):
        layout = QHBoxLayout()
        label = QLabel(name)
        self.labels[name] = label
        self.update_color(name, color)
        layout.addWidget(label)
        btn = QPushButton('Edit')
        btn.clicked.connect(lambda _, pos=name: self.update(pos))
        layout.addWidget(btn)
        self.layout.addLayout(layout)
        
    def update(self, pos):
        color = parse_rgb(QColorDialog.getColor().rgb())
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
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ColorManager(loc='../../style.json')
    ex.show()
    sys.exit(app.exec_())