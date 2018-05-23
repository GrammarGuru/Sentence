from PyQt5.QtWidgets import QLayout
        
def fill_layout(layout, *args):
    for item in args:
        if isinstance(item, QLayout):
            layout.addLayout(item)
        else:
            layout.addWidget(item)
        