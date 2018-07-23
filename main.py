import ctypes
import os
import platform
import sys

from PyQt5.QtWidgets import QApplication

from services import news, web
from src.components.splash import Splash
from src.gui import Model

if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/auth.json'
    if platform.system() == 'Windows':
        my_app_id = 'Technius.GrammarGuru.Sentence'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    app = QApplication(sys.argv)
    
    splash = Splash('assets/splash_logo.png')
    splash.show()
    news_data = news.get_data()
    web_data = web.get_data()
    ex = Model(news_data, web_data)
    ex.show()
    splash.finish(ex)
    sys.exit(app.exec_())
