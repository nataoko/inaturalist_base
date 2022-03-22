# This Python file uses the following encoding: utf-8
# ## luźne pomysły: podświetlenie punktu,
##1. Co ma się dziać po zamknięciu okna Nowy obszar. (zapmknięcie aplikacji)OK
##2. Usunąć wyświetlanie numeru taksonu w nazwach zapisanych obserwacji.
##3. Kwestie usuwania i edycji zapisanych obszarów.
##4. Kopia zapasowa pliku json z zapisanymi danymi. (pierwsza wersja)OK
##5. Skrypt do generowania początkowego pliku json. Obsługa wyjątków w razie błędu pliku json.
# wyświetlanie obszaru, który nie jest spójny
# Uwzględnienie obsługi obszaru: nadpisanie, delecja, wyświetlanie.
# Akceptowalne inne nazwy obszarów (?)
# todo: mapa --- dopasowanie do ekranu
# todo:automatycznie duże guziki i napisy ; layouty zmienić
# todo: style, fontsize

import sys
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QWidget, \
    QPushButton, QLabel, QLineEdit, QFormLayout, QVBoxLayout, QHBoxLayout, \
    QTextEdit, QMessageBox, QInputDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium

from points import valid_list, valid_polygon

from saving import *

DATA = open_data()
ERRORS = {
    'PointList': {
        1: 'Lista ma mniej niż 3 elementy!',
        2: 'Podana długość geograficzna nie jest liczbą.',
        3: 'Podana długość geograficzna spoza zakresu.',
        4: 'Podana szerokość geograficzna nie jest liczbą.',
        5: 'Podana szerokość geograficzna spoza zakresu.',
        6: 'Podana wartość nie jest listą.\nPoprawny format: x, y; x, y ; x, y.\nCzytaj więcej w instrukcji.',
        7: 'Obszar jest wklęsły!',
        8: 'Zły format!\nPoprawny format: x, y; x, y ; x, y.\nCzytaj więcej w instrukcji.',
    },
    'Name': {
        1: 'Nazwa musi zawierać jedynie znaki alfanumeryczne!',
        2: 'Obszar o podanej nazwie istnieje. Wybierz inną nazwę.',
    }
}


def error_show(name, error, name_long):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(f'{name}Error{error}: '
                + ERRORS[name][error])
    msg.setWindowTitle(f'Błąd: {name_long}')
    msg.exec_()


class Menu(QWidget):
    def __init__(self):
        super(Menu, self).__init__()
        self.aboutApp = None
        self.obs = None
        self.newArea = None
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_height = self.screen.height()
        self.screen_width = self.screen.width()
        self.btn_height = int(self.screen_height / 6)
        self.btn_width = int(self.screen_width / 3)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Menu')
        self.setWindowIcon(QIcon('data' + os.sep + 'icon.png'))
        self.resize(self.screen_width, self.screen_height - 100)
        self.move(0, 0)

        # buttons
        new_area_btn = QPushButton(self)
        new_area_btn.setText('Nowy obszar')
        new_area_btn.resize(self.btn_width, self.btn_height)
        new_area_btn.move(self.btn_width, int(self.btn_height / 2))
        new_area_btn.clicked.connect(self.new_area)

        obs_btn = QPushButton(self)
        obs_btn.setText('Obserwacje')
        obs_btn.resize(self.btn_width, self.btn_height)
        obs_btn.move(self.btn_width, self.btn_height * 2)
        obs_btn.clicked.connect(self.observations)

        about_app_btn = QPushButton(self)
        about_app_btn.setText('O Aplikacji')
        about_app_btn.resize(self.btn_width, self.btn_height)
        about_app_btn.move(self.btn_width, int(self.btn_height * 3.5))
        about_app_btn.clicked.connect(self.about_app)

        # version label
        version_label = QLabel(self)
        version_label.setText('v0.0.0')
        version_label.move(self.screen_width - 50, self.screen_height - 120)

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


class NewArea(QWidget):
    def __init__(self, parent=None):
        super(NewArea, self).__init__()
        self.loc = None
        self.setWindowTitle('Nowy obszar')
        self.setWindowIcon(QIcon('data' + os.sep + 'icon.png'))
        self.resize(menu.screen_width, menu.screen_height - 100)
        self.move(0, 0)
        self.data = DATA

        # back button
        back_btn = QPushButton()
        back_btn.setIcon(QIcon('data' + os.sep + 'back.jpg'))
        back_btn.clicked.connect(self.back)

        hbox_back = QHBoxLayout()
        hbox_back.addStretch(1)
        hbox_back.addWidget(back_btn)

        # edit lines
        self.lineLoc = QLineEdit()  #todo: default grey values 10 ,0; 10 ,1;10.5 ,0.5;11 ,1;11 ,0

        flo = QFormLayout()
        flo.addRow('Dane geograficzne', self.lineLoc)

        see_btn = QPushButton(self)
        see_btn.setText('Zobacz wprowadzony obszar')
        see_btn.clicked.connect(self.see_area)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(see_btn)
        hbox.addStretch(1)

        # map
        self.mapa = folium.Map(width=int(menu.screen_width * 0.83),
                               height=int(menu.screen_height * 0.85),
                               location=[0, 10], zoom_start=3)
        folium.TileLayer('cartodbpositron').add_to(self.mapa)
        folium.TileLayer('Stamen Terrain').add_to(self.mapa)
        folium.LayerControl().add_to(self.mapa)
        self.html = self.mapa._repr_html_()

        self.webEngineView = QWebEngineView()
        self.webEngineView.setHtml(self.html)
        # self.webEngineView.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        hbox_map = QHBoxLayout()
        hbox_map.addWidget(self.webEngineView, 1)

        # points list
        self.textEdit = QTextEdit()
        self.textEdit.setPlainText('Lista punktów jest pusta...')  # todo: editable point list

        hbox_map.addWidget(self.textEdit)

        # layout settings
        vbox = QVBoxLayout()
        vbox.addLayout(flo)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_map)
        vbox.addLayout(hbox_back)
        self.setLayout(vbox)

    def back(self):
        menu.show()
        self.hide()

    def save_area(self):  # todo: shortcut alt enter
        area_name, save = QInputDialog.getText(self, 'Zapisywanie obszaru', 'Podaj nazwę')
        if save:
            area_name = 'area' + area_name
            print(str(area_name))
            area_name = valid_name(area_name, self.data)
            try:
                error = int(area_name)
                error_show('Name', error, 'nazwa')
            except:
                self.data = save_new_area(area_name, self.loc, self.data)
                mbox = QMessageBox()
                QMessageBox.setText(mbox, 'Poprawnie zapisano obszar')
                mbox.exec()

    def see_area(self):  # todo: shortcut ctr enter
        lista = valid_list(self.lineLoc.text())
        try:
            error = int(lista)
            error_show('PointList', error, 'dane lokalizacyjne')
        except:
            # point list update
            self.textEdit.setPlainText('\n'.join(map(str, lista)))
            polygon = valid_polygon(lista)
            try:
                error = int(polygon)
                error_show('PointList', error, 'dane lokalizacyjne')
            except:
                # map update #todo: chceck loc what is first here, todo:zoom edit
                self.mapa = folium.Map(width=menu.screen_width - 60,
                                       height=menu.screen_height - 100,
                                       location=lista[0][::-1], zoom_start=5)
                folium.GeoJson(polygon).add_to(self.mapa)
                folium.TileLayer('cartodbpositron').add_to(self.mapa)
                folium.TileLayer('Stamen Terrain').add_to(self.mapa)
                folium.LayerControl().add_to(self.mapa)
                self.html = self.mapa._repr_html_()
                self.webEngineView.setHtml(self.html)
                print('obszar poprawnie skonstruowany')  # todo: error okno zapisać?

                # messagebox
                reppli_msbox = QMessageBox.question(self, 'Poprawnie skonstruowano obszar',
                                                 'Obszar poprawnie skonstruowany.\nAby zapisać, kliknij \"Yes\".',
                                                 QMessageBox.Yes | QMessageBox.Cancel)
                if reppli_msbox == QMessageBox.Yes:
                    self.loc = lista
                    self.save_area()


    def onClick(self):
        pass
        # msgbox = QMessageBox()
        # msgbox.setText('to select click "show details"')
        # msgbox.setTextInteractionFlags(Qt.NoTextInteraction)  # (QtCore.Qt.TextSelectableByMouse)
        # msgbox.setDetailedText('line 1\nline 2\nline 3')
        # msgbox.exec()


class Observations(QWidget):
    def __init__(self, parent=None):
        super(Observations, self).__init__()
        self.setWindowTitle('Obserwacje')
        self.setWindowIcon(QIcon('data' + os.sep + 'icon.png'))
        self.resize(menu.screen_width, menu.screen_height - 100)
        self.move(0, 0)

        # buttons
        backBtn = QPushButton(self)
        backBtn.setIcon(QIcon('data' + os.sep + 'back.jpg'))
        backBtn.resize(int(menu.screen_height * 0.05),
                       int(menu.screen_height * 0.05))
        backBtn.move(int(menu.screen_width * 0.95), int(menu.screen_height * 0.82))
        backBtn.clicked.connect(self.back)

        readFromDiskBtn = QPushButton(self)
        readFromDiskBtn.setText('Wczytaj obserwacje z dysku')
        readFromDiskBtn.resize(menu.btn_width, menu.btn_height)
        readFromDiskBtn.move(menu.btn_width, int(menu.btn_height / 2))
        readFromDiskBtn.clicked.connect(self.read_from_disk)

        generateFromBaseBtn = QPushButton(self)
        generateFromBaseBtn.setText('Generuj obserwacje z bazy')
        generateFromBaseBtn.resize(menu.btn_width, menu.btn_height)
        generateFromBaseBtn.move(menu.btn_width, menu.btn_height * 2)
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
        self.setWindowIcon(QIcon('data' + os.sep + 'icon.png'))
        self.resize(menu.screen_width, menu.screen_height - 100)
        self.move(0, 0)

        backBtn = QPushButton(self)
        backBtn.setIcon(QIcon('data' + os.sep + 'back.jpg'))
        backBtn.resize(int(menu.screen_height * 0.05),
                       int(menu.screen_height * 0.05))
        backBtn.move(int(menu.screen_width * 0.95), int(menu.screen_height * 0.82))
        backBtn.clicked.connect(self.back)

        aboutAppLabel = QLabel(self)
        aboutAppLabel.setText(open('data' + os.sep + 'about_app.txt', 'r',
                                   encoding='UTF-8'
                                   ).read())
        # self.aboutApptLabel.move(int(menu.screen_width*0.01), int(menu.screen_height*0.01))

    def back(self):
        menu.show()
        self.hide()


class ReadFromDisk(QWidget):
    def __init__(self, parent=None):
        super(ReadFromDisk, self).__init__()
        self.setWindowTitle('Wczytaj obserwacje z dysku')
        self.setWindowIcon(QIcon('data' + os.sep + 'icon.png'))
        self.resize(menu.screen_width, menu.screen_height - 100)
        self.move(0, 0)

        # back button
        backBtn = QPushButton(self)
        backBtn.setIcon(QIcon('data' + os.sep + 'back.jpg'))
        backBtn.resize(int(menu.screen_height * 0.05),
                       int(menu.screen_height * 0.05))
        backBtn.move(int(menu.screen_width * 0.95), int(menu.screen_height * 0.82))
        backBtn.clicked.connect(self.back)

    def back(self):
        menu.obs.show()
        self.hide()


class GenerateFromBase(QWidget):
    def __init__(self, parent=None):
        super(GenerateFromBase, self).__init__()
        self.setWindowTitle('Generuj z bazy')
        self.setWindowIcon(QIcon('data' + os.sep + 'icon.png'))
        self.resize(menu.screen_width, menu.screen_height - 100)
        self.move(0, 0)

        # back button
        backBtn = QPushButton(self)
        backBtn.setIcon(QIcon('data' + os.sep + 'back.jpg'))
        backBtn.resize(int(menu.screen_height * 0.05),
                       int(menu.screen_height * 0.05))
        backBtn.move(int(menu.screen_width * 0.95), int(menu.screen_height * 0.82))
        backBtn.clicked.connect(self.back)

    def back(self):
        menu.obs.show()
        self.hide()


if __name__ == '__main__':
    # Stworzenie aplikacji
    app = QApplication(sys.argv)

    # Font settings
    custom_font = QFont()
    # custom_font.setWeight(100)
    custom_font.setPixelSize(20)
    app.setFont(custom_font, 'QLabel')
    app.setFont(custom_font, 'QWidget')

    # Show app
    menu = Menu()
    menu.show()

    # App exit
    sys.exit(app.exec_())
