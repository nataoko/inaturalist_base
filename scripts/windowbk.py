import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QWidget, QPushButton, QHBoxLayout
SCREEN = QDesktopWidget().screenGeometry()
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.width(), SCREEN.height()
    
def menu():
    app = QApplication(sys.argv)
    windows = QWidget()

    # band
    windows.setWindowTitle('Menu')
    windows.setWindowIcon(QIcon('icon.png'))
    
    # full screen

    screen = QDesktopWidget().screenGeometry()
    windows.resize(SCREEN_WIDTH, SCREEN_HEIGHT )
    windows.move(0,0)
    
    windows.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    menu()

    
