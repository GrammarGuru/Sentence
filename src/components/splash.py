from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtGui import QPixmap

class Splash(QSplashScreen):
    def __init__(self, img_loc):
        img = QPixmap(img_loc)
        super().__init__(img)