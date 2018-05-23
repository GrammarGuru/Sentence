import sys
import os
from PyQt5.QtWidgets import QApplication
from src.gui import Model

if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/auth.json'
    app = QApplication(sys.argv)
    ex = Model()

    sys.exit(app.exec_())