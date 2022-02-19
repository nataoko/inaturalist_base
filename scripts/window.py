import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QWidget, QPushButton, QLabel

class Menu(QWidget):
    def __init__(self):
        super(Menu,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Menu")
        self.setWindowIcon(QIcon('icon.png'))
        screen = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen.width(), screen.height()
        self.resize(screen_width, screen_height-100)
        self.move(0,0)

        button_width, button_height = int(screen_width/3), int(screen_height/6)
        
        self.newAreaButton = QPushButton(self)
        self.newAreaButton.setText("Nowy obszar")          
        self.newAreaButton.resize(button_width, button_height)
        self.newAreaButton.move(button_width, int(button_height/2))
        self.newAreaButton.clicked.connect(self.new_area)

        self.observationsButton = QPushButton(self)
        self.observationsButton.setText("Obserwacje")          
        self.observationsButton.resize(button_width, button_height)
        self.observationsButton.move(button_width, button_height*2)

        self.aboutAplicationButton = QPushButton(self)
        self.aboutAplicationButton.setText("O Aplikacji")          
        self.aboutAplicationButton.resize(button_width, button_height)
        self.aboutAplicationButton.move(button_width, int(button_height*3.5))

        self.versiontLabel = QLabel(self)
        self.versiontLabel.setText("v0.0.0")
        self.versiontLabel.move(screen_width-50, screen_height-120)

    def new_area(self):        
        newArea = NewArea()
        newArea.show()

class NewArea(QWidget):
    def __init__(self):
        super(NewArea, self).__init__()
        self.setWindowTitle('Nowy obszar')
        self.setWindowIcon(QIcon('icon.png'))
        screen = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen.width(), screen.height()
        self.resize(screen_width, screen_height-100)
        self.move(0,0)

class ReadFromDisc(QWidget):
    def __init__(self):
        super(ReadFromDisc, self).__init__()
        self.setWindowTitle('Wczytaj obserwacje z dysku')
        self.setWindowIcon(QIcon('icon.png'))
        screen = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen.width(), screen.height()
        self.resize(screen_width, screen_height-100)
        self.move(0,0)

class GenerateFromBase(QWidget):
    def __init__(self):
        super(ReadFromDisc, self).__init__()
        self.setWindowTitle('Generuj z bazy')
        self.setWindowIcon(QIcon('icon.png'))
        screen = QDesktopWidget().screenGeometry()
        #screen_width, screen_height = screen.width(), screen.height()
        self.resize(screen_width, screen_height-100)
        self.move(0,0)

class Observations(QWidget):
    def __init__(self):
        super(ReadFromDisc, self).__init__()
        self.setWindowTitle('Obserwacje')
        self.setWindowIcon(QIcon('icon.png'))
        screen = QDesktopWidget().screenGeometry()
        #screen_width, screen_height = screen.width(), screen.height()
        self.resize(screen_width, screen_height-100)
        self.move(0,0)

class Error(QWidget):
    def __init__(self):
        super(ReadFromDisc, self).__init__()
        self.setWindowTitle('Błąd')
        self.setWindowIcon(QIcon('icon.png'))
        screen = QDesktopWidget().screenGeometry()
        #screen_width, screen_height = screen.width(), screen.height()
        #self.resize(screen_width, screen_height-100)
        #self.move(screen_width, screen_height-100)
    

#todo: Okno wprowadzania obszaru
#todo: style

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = Menu()
    menu.show()
    sys.exit(app.exec_())

    
