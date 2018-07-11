import sys
import os
import ctypes
from PyQt5.QtWidgets import QApplication
from src.gui import Model
from src.components.splash import Splash
from src.api.news import get_data


if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/auth.json'
    my_app_id = 'Technius.GrammarGuru.Sentence'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    app = QApplication(sys.argv)
    
    splash = Splash('assets/splash_logo.png')
    splash.show()
    data = get_data()
    ex = Model(data)
    ex.show()
    splash.finish(ex)
    sys.exit(app.exec_())