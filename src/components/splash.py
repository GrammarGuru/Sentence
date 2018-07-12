from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen


class Splash(QSplashScreen):
    def __init__(self, img_loc):
        img = QPixmap(img_loc)
        super().__init__(img)
