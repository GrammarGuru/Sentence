import sys
import os
from PyQt5.QtWidgets import QApplication
from src.gui import Model
from src.components.splash import Splash

if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/auth.json'
    app = QApplication(sys.argv)
    
    splash = Splash('images/splash_logo.png')
    splash.show()
    ex = Model()
    ex.show()
    splash.finish(ex)
    sys.exit(app.exec_())