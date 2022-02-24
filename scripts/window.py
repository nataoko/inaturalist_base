import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget, QApplication,\
                            QWidget, QPushButton, QLabel,\
                            QLineEdit, QFormLayout,\
                            QVBoxLayout, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium
import io

class Menu(QWidget):
    def __init__(self):
        super(Menu,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Menu")
        self.setWindowIcon(QIcon('icon.png'))
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width = self.screen.width()
        self.screen_height = self.screen.height()
        self.resize(self.screen_width, self.screen_height-100)
        self.move(0,0)

        self.button_width = int(self.screen_width/3) 
        self.button_height = int(self.screen_height/6)

        # buttons
        newAreaButton = QPushButton(self)
        newAreaButton.setText("Nowy obszar")          
        newAreaButton.resize(self.button_width,
                             self.button_height)
        newAreaButton.move(self.button_width,
                           int(self.button_height/2))
        newAreaButton.clicked.connect(self.new_area)

        observationsButton = QPushButton(self)
        observationsButton.setText("Obserwacje")          
        observationsButton.resize(self.button_width,
                                  self.button_height)
        observationsButton.move(self.button_width,
                                self.button_height*2)
        observationsButton.clicked.connect(self.observations)
        
        aboutAplicationButton = QPushButton(self)
        aboutAplicationButton.setText("O Aplikacji")          
        aboutAplicationButton.resize(self.button_width,
                                     self.button_height)
        aboutAplicationButton.move(self.button_width,
                                   int(self.button_height*3.5))
        aboutAplicationButton.clicked.connect(self.about_app)

        # version label
        versionLabel = QLabel(self)
        versionLabel.setText("v0.0.0")
        versiontLabel.move(self.screen_width-50,
                                self.screen_height-120)
        
##        hbox = QHBoxLayout()
##        hbox.addStretch(1)
##        hbox.addWidget(versionLabel)
##
##        # layoutsettiongs
##        vbox = QHBoxLayout()
##        hbox.addStretch(1)
##        vbox.addLayout(hbox)
##        self.setLayout(vbox)
        
    def new_area(self):        
        self.newArea = NewArea(self)
        self.newArea.show()
        self.hide()

    def observations(self):
        self.obs = Observations(self)
        self.obs.show()        
        self.hide()

    def about_app(self):
        self.aboutApp = AboutApp(self)
        self.aboutApp.show()        
        self.hide()

    def error(self):
        self.er = Error(self)
        self.er.show()        

class NewArea(QWidget):
    def __init__(self, parent=None):
        super(NewArea, self).__init__()
        self.setWindowTitle('Nowy obszar')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(menu.screen_width, menu.screen_height-100)
        self.move(0,0)
        
        # back button
        backButton = QPushButton()
        backButton.setIcon(QIcon("back.jpg"))
        backButton.clicked.connect(self.back)
        
        hboxback = QHBoxLayout()
        hboxback.addStretch(1)
        hboxback.addWidget(backButton)

        # edit lines
        lineName = QLineEdit()
        lineLoc = QLineEdit()
        
        flo = QFormLayout()
        flo.addRow("Nazwa obszaru",lineName)
        flo.addRow("Dane geograficzne",lineLoc)

        # save and see buttons
        saveButton = QPushButton(self)
        saveButton.setText("Zapisz wprowadzony obszar")
        saveButton.clicked.connect(self.save_area)

        seeButton = QPushButton(self)
        seeButton.setText("Zobacz wprowadzony obszar")
        seeButton.clicked.connect(self.see_area)

        hbox = QHBoxLayout()
        hbox.addWidget(saveButton)
        hbox.addWidget(seeButton)

        # map
        mapa = folium.Map(width=500, height=400,
                          location=[0,10], zoom_start=5)
        folium.TileLayer('cartodbpositron').add_to(mapa)
        folium.TileLayer('Stamen Terrain').add_to(mapa)
        folium.LayerControl().add_to(mapa)
        html = mapa._repr_html_()

        self.webEngineView = QWebEngineView()
        self.webEngineView.setHtml(html)

        # layout settings
        vbox = QVBoxLayout()
        vbox.addLayout(flo)
        vbox.addLayout(hbox)
        vbox.addWidget(self.webEngineView)
        vbox.addLayout(hboxback)
        self.setLayout(vbox)

    def back(self):        
        menu.show()
        self.hide()

    def save_area(self):
        pass

    def see_area(self):
        pass

class Observations(QWidget):
    def __init__(self, parent=None):
        super(Observations, self).__init__()
        self.setWindowTitle('Obserwacje')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(menu.screen_width, menu.screen_height-100)
        self.move(0,0)

        # buttons
        backButton = QPushButton(self)
        backButton.setIcon(QIcon("back.jpg"))
        backButton.resize(int(menu.screen_height*0.05),
                               int(menu.screen_height*0.05))
        backButton.move(int(menu.screen_width*0.95),
                             int(menu.screen_height*0.82))
        backButton.clicked.connect(self.back)

        readFromDiskButton = QPushButton(self)
        readFromDiskButton.setText("Wczytaj obserwacje z dysku")          
        readFromDiskButton.resize(menu.button_width,
                                       menu.button_height)
        readFromDiskButton.move(menu.button_width,
                                     int(menu.button_height/2))
        readFromDiskButton.clicked.connect(self.read_from_disk)

        generateFromBaseButton = QPushButton(self)
        generateFromBaseButton.setText("Generuj obserwacje z bazy")          
        generateFromBaseButton.resize(menu.button_width,
                                           menu.button_height)
        generateFromBaseButton.move(menu.button_width,
                                         menu.button_height*2)
        generateFromBaseButton.clicked.connect(self.generate_from_base)
        
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
        super(AboutApp, self).__init__()
        self.setWindowTitle('O Aplikacji')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(menu.screen_width, menu.screen_height-100)
        self.move(0,0)

        backButton = QPushButton(self)
        backButton.setIcon(QIcon("back.jpg"))
        backButton.resize(int(menu.screen_height*0.05),
                               int(menu.screen_height*0.05))
        backButton.move(int(menu.screen_width*0.95),
                            int(menu.screen_height*0.82))
        backButton.clicked.connect(self.back)

        aboutAppLabel = QLabel(self)
        aboutAppLabel.setText(open("about_app.txt", "r",
                                        encoding='UTF-8').read())
        #self.aboutApptLabel.move(int(menu.screen_width*0.01), int(menu.screen_height*0.01))

    def back(self):
        menu.show()
        self.hide()

class ReadFromDisk(QWidget):
    def __init__(self, parent=None):
        super(ReadFromDisk, self).__init__()
        self.setWindowTitle('Wczytaj obserwacje z dysku')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(menu.screen_width, menu.screen_height-100)
        self.move(0,0)

        # back button
        backButton = QPushButton(self)
        backButton.setIcon(QIcon("back.jpg"))
        backButton.resize(int(menu.screen_height*0.05),
                          int(menu.screen_height*0.05))
        backButton.move(int(menu.screen_width*0.95),
                        int(menu.screen_height*0.82))
        backButton.clicked.connect(self.back)

    def back(self):        
        menu.obs.show()
        self.hide()

class GenerateFromBase(QWidget):
    def __init__(self, parent=None):
        super(GenerateFromBase, self).__init__()
        self.setWindowTitle('Generuj z bazy')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(menu.screen_width, menu.screen_height-100)
        self.move(0,0)

        # back button
        backButton = QPushButton(self)
        backButton.setIcon(QIcon("back.jpg"))
        backButton.resize(int(menu.screen_height*0.05),
                               int(menu.screen_height*0.05))
        backButton.move(int(menu.screen_width*0.95),
                             int(menu.screen_height*0.82))
        backButton.clicked.connect(self.back)

    def back(self):        
        menu.obs.show()
        self.hide()

class Error(QWidget):
    def __init__(self):
        super(ReadFromDisc, self).__init__()
        self.setWindowTitle('Błąd')
        self.setWindowIcon(QIcon('icon.png'))
    

#todo: Okno wprowadzania obszaru
#todo: style

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = Menu()
    menu.show()
    sys.exit(app.exec_())

    
