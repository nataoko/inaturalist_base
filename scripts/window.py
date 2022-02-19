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
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width, self.screen_height = self.screen.width(), self.screen.height()
        self.resize(self.screen_width, self.screen_height-100)
        self.move(0,0)

        self.button_width, self.button_height = int(self.screen_width/3), int(self.screen_height/6)
        
        self.newAreaButton = QPushButton(self)
        self.newAreaButton.setText("Nowy obszar")          
        self.newAreaButton.resize(self.button_width, self.button_height)
        self.newAreaButton.move(self.button_width, int(self.button_height/2))
        self.newAreaButton.clicked.connect(self.new_area)

        self.observationsButton = QPushButton(self)
        self.observationsButton.setText("Obserwacje")          
        self.observationsButton.resize(self.button_width, self.button_height)
        self.observationsButton.move(self.button_width, self.button_height*2)
        self.observationsButton.clicked.connect(self.observations)
        
        self.aboutAplicationButton = QPushButton(self)
        self.aboutAplicationButton.setText("O Aplikacji")          
        self.aboutAplicationButton.resize(self.button_width, self.button_height)
        self.aboutAplicationButton.move(self.button_width, int(self.button_height*3.5))
        self.aboutAplicationButton.clicked.connect(self.new_area)

        self.versiontLabel = QLabel(self)
        self.versiontLabel.setText("v0.0.0")
        self.versiontLabel.move(self.screen_width-50, self.screen_height-120)

    def new_area(self):        
        self.newArea = NewArea(self)
        self.newArea.show()
        self.hide()

    def observations(self):
        self.obs = Observations(self)
        self.obs.show()        
        self.hide()

    def error(self):
        self.er = Error(self)
        self.er.show()        

class NewArea(QWidget):
    def __init__(self, parent=None):
        super(NewArea, self).__init__()
        self.setWindowTitle('Nowy obszar')
        self.setWindowIcon(QIcon('icon.png'))
##        self.screen = QDesktopWidget().screenGeometry()
##        self.screen_width, self.screen_height = self.screen.width(), self.screen.height()
        self.resize(menu.screen_width, menu.screen_height-100)
        self.move(0,0)
        
        self.backButton = QPushButton(self)
        self.backButton.setIcon(QIcon("back.jpg"))
        self.backButton.resize(int(menu.screen_height*0.05), int(menu.screen_height*0.05))
        self.backButton.move(int(menu.screen_width*0.95), int(menu.screen_height*0.82))
        self.backButton.clicked.connect(self.back)

    def back(self):        
        menu.show()
        self.hide()

class Observations(QWidget):
    def __init__(self, parent=None):
        super(Observations, self).__init__()
        self.setWindowTitle('Obserwacje')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(menu.screen_width, menu.screen_height-100)
        self.move(0,0)

        self.backButton = QPushButton(self)
        self.backButton.setIcon(QIcon("back.jpg"))
        self.backButton.resize(int(menu.screen_height*0.05), int(menu.screen_height*0.05))
        self.backButton.move(int(menu.screen_width*0.95), int(menu.screen_height*0.82))
        self.backButton.clicked.connect(self.back)
        
    def read_from_disk(self):        
        self.readFromDisk = ReadFromDisk(self)
        self.readFromDisk.show()
        self.hide()

    def generate_from_base(self):        
        self.generateFromBase = GenerateFromBase(self)
        self.generateFromBase.show()
        self.hide()

    def back(self):        
        menu.show()
        self.hide()

class AboutApp(QWidget):
    def __init__(self, parent=None):
        super(Observations, self).__init__()
        self.setWindowTitle('O Aplikacji')
        self.setWindowIcon(QIcon('icon.png'))
        screen = QDesktopWidget().screenGeometry()
        screen_width, screen_height = menu.screen.width(), menu.screen.height()
        self.resize(screen_width, screen_height-100)
        self.move(0,0)

        self.backButton = QPushButton(self)
        self.backButton.setIcon(QIcon("back.jpg"))
        self.backButton.resize(int(menu.screen_height*0.05), int(menu.screen_height*0.05))
        self.backButton.move(int(menu.screen_width*0.95), int(menu.screen_height*0.82))
        self.backButton.clicked.connect(self.back)

    def back(self):        
        menu.show()
        self.hide()

class ReadFromDisk(QWidget):
    def __init__(self, parent=None):
        super(ReadFromDisc, self).__init__()
        self.setWindowTitle('Wczytaj obserwacje z dysku')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(menu.screen_width, menu.screen_height-100)
        self.move(0,0)

class GenerateFromBase(QWidget):
    def __init__(self, parent=None):
        super(ReadFromDisc, self).__init__()
        self.setWindowTitle('Generuj z bazy')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(menu.screen_width, menu.screen_height-100)
        self.move(0,0)

class Error(QWidget):
    def __init__(self):
        super(ReadFromDisc, self).__init__()
        self.setWindowTitle('Błąd')
        self.setWindowIcon(QIcon('icon.png'))
    

#todo: Okno wprowadzania obszaru
#todo: style
#dziedziczenie zmiennych po głównym

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = Menu()
    menu.show()
    sys.exit(app.exec_())

    
