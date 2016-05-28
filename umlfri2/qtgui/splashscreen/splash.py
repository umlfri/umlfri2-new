import os.path
from time import time

from PySide.QtCore import QTimer
from PySide.QtGui import QSplashScreen, QPixmap, QFont, QColor, QPen

from umlfri2.application import Application
from umlfri2.constants.paths import GRAPHICS
from umlfri2.constants.splashscreen import SPLASH_TIMEOUT
from umlfri2.qtgui.mainwindow import UmlFriMainWindow


class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap(os.path.join(GRAPHICS, "splash", "splash.png")))
        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__timer_event)
        self.__timeout = time() + SPLASH_TIMEOUT / 1000
        self.__timer.start(100)
        self.__timer_event()
    
    def __timer_event(self):
        if self.__timeout < time():
            self.__timer.stop()
            main_window = UmlFriMainWindow()
            main_window.showMaximized()
            self.finish(main_window)
    
    def drawContents(self, painter):
        qfont = QFont("Arial")
        qfont.setPixelSize(12.5)
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(qfont)
        painter.drawText(300, 150, "Version: {0}".format(Application().VERSION))
