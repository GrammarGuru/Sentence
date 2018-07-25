import sys
import platform
import os
import ctypes
import logging

from PyQt5.QtWidgets import QApplication

from services import news, web
from src.components.splash import Splash
from src.gui import Model

def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))


logger = logging.getLogger('logs')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logs.txt')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

# Install exception handler
sys.excepthook = my_handler

if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/auth.json'
    if platform.system() == 'Windows':
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