#luźne pomysły: podświetlenie punktu

import sys
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QWidget,\
    QPushButton, QLabel, QLineEdit, QFormLayout, QVBoxLayout, QHBoxLayout,\
    QSizePolicy, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium
import io

from points import valid_list, valid_polygon

class Menu(QWidget):
    def __init__(self):
        super(Menu,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Menu')
        self.setWindowIcon(QIcon('icon.png'))
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_width = self.screen.width()
        self.screen_height = self.screen.height()
        self.resize(self.screen_width, self.screen_height-100)
        self.move(0,0)

        self.btn_width = int(self.screen_width/3) 
        self.btn_height = int(self.screen_height/6)

        # buttons
        newAreaBtn = QPushButton(self)
        newAreaBtn.setText('Nowy obszar')          
        newAreaBtn.resize(self.btn_width, self.btn_height)
        newAreaBtn.move(self.btn_width, int(self.btn_height/2))
        newAreaBtn.clicked.connect(self.new_area)

        obsBtn = QPushButton(self)
        obsBtn.setText('Obserwacje')          
        obsBtn.resize(self.btn_width, self.btn_height)
        obsBtn.move(self.btn_width, self.btn_height*2)
        obsBtn.clicked.connect(self.observations)
        
        aboutAppBtn = QPushButton(self)
        aboutAppBtn.setText('O Aplikacji')          
        aboutAppBtn.resize(self.btn_width, self.btn_height)
        aboutAppBtn.move(self.btn_width, int(self.btn_height*3.5))
        aboutAppBtn.clicked.connect(self.about_app)

        # version label
        versionLabel = QLabel(self)
        versionLabel.setText('v0.0.0')
        versionLabel.move(self.screen_width-50,
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
        backBtn = QPushButton()
        backBtn.setIcon(QIcon('back.jpg'))
        backBtn.clicked.connect(self.back)
        
        hboxback = QHBoxLayout()
        hboxback.addStretch(1)
        hboxback.addWidget(backBtn)

        # edit lines
        lineName = QLineEdit()
        #lineName.setInputMask('Park krajobrazowy A')
        self.lineLoc = QLineEdit()#10 ,0; 10 ,1;10.5 ,0.5;11 ,1;11 ,0
        
        flo = QFormLayout()
        flo.addRow('Nazwa obszaru',lineName)
        flo.addRow('Dane geograficzne',self.lineLoc)

        # save and see buttons
        saveBtn = QPushButton(self)
        saveBtn.setText('Zapisz wprowadzony obszar')
        saveBtn.clicked.connect(self.save_area)

        seeBtn = QPushButton(self)
        seeBtn.setText('Zobacz wprowadzony obszar')
        seeBtn.clicked.connect(self.see_area)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(saveBtn)
        hbox.addStretch(1)
        hbox.addWidget(seeBtn)
        hbox.addStretch(1)

        # map
        self.mapa = folium.Map(width=menu.screen_width-60,
                          height=menu.screen_height-100,
                          location=[0,10], zoom_start=2)
        folium.TileLayer('cartodbpositron').add_to(self.mapa)
        folium.TileLayer('Stamen Terrain').add_to(self.mapa)
        folium.LayerControl().add_to(self.mapa)
        self.html = self.mapa._repr_html_()

        self.webEngineView = QWebEngineView()
        self.webEngineView.setHtml(self.html)
        #self.webEngineView.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        hboxmap = QHBoxLayout()
        hboxmap.addWidget(self.webEngineView, 1)

        # points list
        self.textEdit = QTextEdit()
        self.textEdit.setPlainText('Lista punktów jest pusta...')#todo: edit or not

        hboxmap.addWidget(self.textEdit)

        # layout settings
        vbox = QVBoxLayout()
        vbox.addLayout(flo)
        vbox.addLayout(hbox)
        vbox.addLayout(hboxmap)
        #vbox.addWidget(self.webEngineView, 1)
        vbox.addLayout(hboxback)
        self.setLayout(vbox)

    def back(self):        
        menu.show()
        self.hide()

    def save_area(self):# todo: shortcut alt enter
        pass

    def see_area(self):# todo: shortcut ctr enter
        lista = valid_list(self.lineLoc.text())
        try:
            error = int(lista)
            print(error)#todo: error okno
        except:
            # point list update
            self.textEdit.setPlainText('\n'.join(map(str, lista)))
            
            # map update #todo: chceck loc what is first here, todo:zoom edit
            self.textEdit.setPlainText('\n'.join(map(str, lista)))
            self.mapa = folium.Map(width=menu.screen_width-60,
                          height=menu.screen_height-100,
                          location=lista[0][::-1], zoom_start=5)
            polygon = valid_polygon(lista)
            folium.GeoJson(polygon).add_to(self.mapa)
            folium.TileLayer('cartodbpositron').add_to(self.mapa)
            folium.TileLayer('Stamen Terrain').add_to(self.mapa)
            folium.LayerControl().add_to(self.mapa)
            self.html = self.mapa._repr_html_()
            self.webEngineView.setHtml(self.html)
            try:
                error = int(polygon)
                print(error)#todo: error okno
            except:
                print('obszar poprawnie skonstruowany')#todo: error okno               

class Observations(QWidget):
    def __init__(self, parent=None):
        super(Observations, self).__init__()
        self.setWindowTitle('Obserwacje')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(menu.screen_width, menu.screen_height-100)
        self.move(0,0)

        # buttons
        backBtn = QPushButton(self)
        backBtn.setIcon(QIcon('back.jpg'))
        backBtn.resize(int(menu.screen_height*0.05),
                       int(menu.screen_height*0.05))
        backBtn.move(int(menu.screen_width*0.95), int(menu.screen_height*0.82))
        backBtn.clicked.connect(self.back)

        readFromDiskBtn = QPushButton(self)
        readFromDiskBtn.setText('Wczytaj obserwacje z dysku')          
        readFromDiskBtn.resize(menu.btn_width, menu.btn_height)
        readFromDiskBtn.move(menu.btn_width, int(menu.btn_height/2))
        readFromDiskBtn.clicked.connect(self.read_from_disk)

        generateFromBaseBtn = QPushButton(self)
        generateFromBaseBtn.setText('Generuj obserwacje z bazy')          
        generateFromBaseBtn.resize(menu.btn_width, menu.btn_height)
        generateFromBaseBtn.move(menu.btn_width, menu.btn_height*2)
        generateFromBaseBtn.clicked.connect(self.generate_from_base)
        
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

        backBtn = QPushButton(self)
        backBtn.setIcon(QIcon('back.jpg'))
        backBtn.resize(int(menu.screen_height*0.05),
                       int(menu.screen_height*0.05))
        backBtn.move(int(menu.screen_width*0.95), int(menu.screen_height*0.82))
        backBtn.clicked.connect(self.back)

        aboutAppLabel = QLabel(self)
        aboutAppLabel.setText(open('about_app.txt', 'r',
                                   encoding='UTF-8'
                                   ).read())
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
        backBtn = QPushButton(self)
        backBtn.setIcon(QIcon('back.jpg'))
        backBtn.resize(int(menu.screen_height*0.05),
                       int(menu.screen_height*0.05))
        backBtn.move(int(menu.screen_width*0.95), int(menu.screen_height*0.82))
        backBtn.clicked.connect(self.back)

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
        backBtn = QPushButton(self)
        backBtn.setIcon(QIcon('back.jpg'))
        backBtn.resize(int(menu.screen_height*0.05),
                       int(menu.screen_height*0.05))
        backBtn.move(int(menu.screen_width*0.95), int(menu.screen_height*0.82))
        backBtn.clicked.connect(self.back)

    def back(self):        
        menu.obs.show()
        self.hide()

class Error(QWidget):
    def __init__(self):
        super(ReadFromDisc, self).__init__()
        self.setWindowTitle('Błąd')
        self.setWindowIcon(QIcon('icon.png'))
    

#todo: mapa --- dopadowanie do ekranu
        #todo:automatycznie duże guziki i napisy ; layouty zmienić
#todo: style, fontsize

if __name__ == '__main__':
    #custom_font = QFont()
    #custom_font.setWeight(100);
    app = QApplication(sys.argv)
    #app.setFont(custom_font, 'QLabel')
    menu = Menu()
    menu.show()
    sys.exit(app.exec_())
   
