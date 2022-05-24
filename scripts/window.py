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
    QTextEdit, QMessageBox, QInputDialog, QDateEdit, QComboBox, QGridLayout, \
    QCheckBox, QCompleter, QListWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import folium

from my_ipyplot import my_plot_images
from validation import valid_list, valid_polygon, valid_name, Polygon, mapping, Point
from saving import *
from inaturalist import *

try:
    DATA = open_data()
except:
    DATA = gen_if_error()

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
    },
    'Taxon': {
        1: 'Nazwa musi być podświetlona na zielono.'
    }
}


def error_show(name, error, name_long):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(f'{name}Error{error}: ' + ERRORS[name][error])
    msg.setWindowTitle(f'Błąd: {name_long}')
    msg.exec_()


class Menu(QWidget):
    def __init__(self):
        super(Menu, self).__init__()
        self.aboutApp = None
        self.generate_from_base_win = None
        self.newArea = None
        self.screen = QDesktopWidget().screenGeometry()
        self.screen_height = self.screen.height()
        self.screen_width = self.screen.width()
        self.btn_height = int(self.screen_height / 6)
        self.btn_width = int(self.screen_width / 3)
        self.initUI()
        self.data = DATA

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
        self.generate_from_base_win = GenerateFromBase(self)
        self.generate_from_base_win.show()
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
        self.lineLoc = QLineEdit()  # todo: default grey values 10 ,0; 10 ,1;10.5 ,0.5;11 ,1;11 ,0

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
        folium.LatLngPopup().add_to(self.mapa)
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
                folium.LatLngPopup().add_to(self.mapa)
                self.html = self.mapa._repr_html_()
                self.webEngineView.setHtml(self.html)
                print('obszar poprawnie skonstruowany')  # todo: error okno zapisać?

                # messagebox
                repply_msbox = QMessageBox.question(self, 'Poprawnie skonstruowano obszar',
                                                    'Obszar poprawnie skonstruowany.\nAby zapisać, kliknij \"Yes\".',
                                                    QMessageBox.Yes | QMessageBox.Cancel)
                if repply_msbox == QMessageBox.Yes:
                    self.loc = lista
                    self.save_area()


class AboutApp(QWidget):
    def __init__(self, parent=None):
        super(AboutApp, self).__init__()
        self.setWindowTitle('O Aplikacji')
        self.setWindowIcon(QIcon('data' + os.sep + 'icon.png'))
        self.resize(menu.screen_width, menu.screen_height - 100)
        self.move(0, 0)

        back_btn = QPushButton(self)
        back_btn.setIcon(QIcon('data' + os.sep + 'back.jpg'))
        back_btn.resize(int(menu.screen_height * 0.05),
                        int(menu.screen_height * 0.05))
        back_btn.move(int(menu.screen_width * 0.95), int(menu.screen_height * 0.82))
        back_btn.clicked.connect(self.back)

        about_app_label = QLabel(self)
        about_app_label.setText(open('data' + os.sep + 'about_app.txt', 'r',
                                     encoding='UTF-8'
                                     ).read())
        # self.aboutApptLabel.move(int(menu.screen_width*0.01), int(menu.screen_height*0.01))

    def back(self):
        menu.show()
        self.hide()


class GenerateFromBase(QWidget):
    def __init__(self, parent=None):
        super(GenerateFromBase, self).__init__()
        #self.threatened = 0
        self.show_obs = None
        self.valid_name = False
        self.names = []
        self.names_long = []
        self.setWindowTitle('Generuj z bazy')
        self.setWindowIcon(QIcon('data' + os.sep + 'icon.png'))
        self.resize(menu.screen_width, menu.screen_height - 100)
        self.move(0, 0)
        self.countries = None

        # back button
        back_btn = QPushButton(self)
        back_btn.setIcon(QIcon('data' + os.sep + 'back.jpg'))
        back_btn.resize(int(menu.screen_height * 0.05), int(menu.screen_height * 0.05))
        back_btn.move(int(menu.screen_width * 0.95), int(menu.screen_height * 0.82))
        back_btn.clicked.connect(self.back)

        hbox_back = QHBoxLayout()
        hbox_back.addStretch(1)
        hbox_back.addWidget(back_btn)

#todo: del self.data in new Area

        self.date_from = QDateEdit(calendarPopup=True)
        self.date_from.setDateTime(QDateTime.currentDateTime().addDays(-2))

        self.date_to = QDateEdit(calendarPopup=True)
        self.date_to.setDateTime(QDateTime.currentDateTime())

        self.checkBoxA = QCheckBox('Takson', self)
        self.checkBoxB = QCheckBox('Nazwa', self)
        self.checkBoxA.stateChanged.connect(self.uncheck)
        self.checkBoxB.stateChanged.connect(self.uncheck)
        hbox_tn = QHBoxLayout()
        hbox_tn.addWidget(self.checkBoxA)
        hbox_tn.addWidget(self.checkBoxB)

        self.ledit_name = QLineEdit()
        self.ledit_name.textChanged.connect(self.text_changed)
        self.autocomplete_model = QStandardItemModel()
        self.completer = QCompleter()
        self.completer.setModel(self.autocomplete_model)
        self.ledit_name.setCompleter(self.completer)

        self.checkBoxT = QCheckBox("Tylko zagrożone", self)
        #self.checkBoxT.stateChanged.connect(self.check_t)

        self.checkBoxArea = QCheckBox('', self)

        self.cb = QComboBox()
        self.cb.addItems(menu.data['areas'].keys())
        self.countries = gen_countries()
        self.cb.addItems(self.countries.keys())

        self.cb.currentIndexChanged.connect(self.selection_change)

        gen_btn = QPushButton(self)
        gen_btn.setText('Generuj obserwacje')
        gen_btn.clicked.connect(self.gen)

        grid = QGridLayout()
        text_from = QLabel(self)
        text_from.setText('Od:')
        grid.addWidget(text_from, 0, 0)
        text_to = QLabel(self)
        text_to.setText('Do:')
        grid.addWidget(text_to, 1, 0)
        text_name = QLabel('Takson/Nazwa:')
        grid.addWidget(text_name,2, 0)
        text_th = QLabel('Zagrożony gatunek: ')
        grid.addWidget(text_th, 4, 0)
        text_area_check = QLabel(self)
        text_area_check.setText('Tylko obszar:')
        grid.addWidget(text_area_check, 5, 0)
        text_area = QLabel(self)
        text_area.setText('Obszar:')
        grid.addWidget(text_area, 6, 0)

        grid.addWidget(self.date_from, 0, 1)
        grid.addWidget(self.date_to, 1, 1)
        grid.addLayout(hbox_tn, 2, 1)
        grid.addWidget(self.ledit_name, 3, 1)
        grid.addWidget(self.checkBoxT, 4, 1)
        grid.addWidget(self.checkBoxArea, 5, 1)
        grid.addWidget(self.cb, 6, 1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(grid)
        hbox.addStretch(1)

        hbox_gen = QHBoxLayout()
        hbox_gen.addStretch(1)
        hbox_gen.addWidget(gen_btn)
        hbox_gen.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_gen)
        vbox.addStretch(1)
        vbox.addLayout(hbox_back)
        self.setLayout(vbox)

        # todo: str18

#    def check_t(self):
#        self.threatened = (self.threatened + 1) % 2
#        print(self.threatened)

    def text_changed(self):
        txt = self.ledit_name.text().lower()
        if len(txt) == 1:
            if 48 <= ord(txt[0]) <= 57:
                self.checkBoxA.setChecked(True)
            elif 97 <= ord(txt[0]) <= 122:
                self.checkBoxB.setChecked(True)
            #else:
            #    self.ledit_name.setStyleSheet("QLineEdit"
            #                            "{"
            #                            "background : lightred;"
            #                            "}")

        if self.checkBoxB.isChecked():
            if '|' not in txt:
                self.names = [i.split(': ')[1].split(' ', 1)[0].lower() for i in map(str, name_list(txt))]
                self.names_long = [i.split(': ')[1].split(' ', 1)[0].lower()+'|'+i for i in map(str, name_list(txt))]
        elif self.checkBoxA.isChecked():
            try:
                self.names = [i.split(']', 1)[0][1:].lower() for i in map(str, taxon_list(txt))]
                self.names_long = [i.split(']', 1)[0][1:].lower()+'|'+i for i in map(str, taxon_list(txt))]
            except:
                self.ledit_name.setStyleSheet("QLineEdit"
                                              "{"
                                              "background : white;"
                                              "}")
                self.names = []
                self.names_long = []
        for item in self.names_long:
            if not self.autocomplete_model.findItems(item):
                self.autocomplete_model.appendRow(QStandardItem(item))
        #print(txt.split('|')[0] in self.names, txt.split('|')[0], self.names)
        if txt.split('|')[0] in self.names:
            self.ledit_name.setStyleSheet("QLineEdit"
                                          "{"
                                          "background : lightgreen;"
                                          "}")
            self.valid_name = True
        else:
            self.ledit_name.setStyleSheet("QLineEdit"
                                          "{"
                                          "background : white;"
                                          "}")
            self.valid_name = False

    def gen(self):
        d1 = self.date_from.date().toPyDate()
        d2 = self.date_to.date().toPyDate()
        txt = self.ledit_name.text().split('|')[0]
        if self.valid_name:
            if self.checkBoxB.isChecked():
                obs = gen_obs_name(txt, d1, d2, int(self.checkBoxT.isChecked()))
            else:
                obs = gen_obs_taxon(txt, d1, d2, int(self.checkBoxT.isChecked()))
        else:
            error_show('Taxon', 1, 'taxon')
        try:
            area = Polygon(menu.data['areas'][self.cb.currentText()])
        except:
            area = self.countries[self.cb.currentText()]
        self.show_obs = ShowObs(txt, d1, d2, self.cb.currentText(), obs, area, int(self.checkBoxT.isChecked()),
                                self.checkBoxArea.isChecked())
        self.show_obs.show()
        #self.hide()
        # todo: container
        #menu.obs.generate_from_base()
        #menu.obs.generate_from_base_win.show()

    # uncheck method
    def uncheck(self, state):

        # checking if state is checked
        if state == Qt.Checked:

            # if first check box is selected
            if self.sender() == self.checkBoxB:
                # making other check box to uncheck
                self.checkBoxA.setChecked(False)

            # if second check box is selected
            elif self.sender() == self.checkBoxA:
                # making other check box to uncheck
                self.checkBoxB.setChecked(False)

    def selection_change(self, i):
        #print("Items in the list are :")

        for count in range(self.cb.count()):
            print(self.cb.itemText(count))
        print("Current index", i, "selection changed ", self.cb.currentText())
        #self.area = self.cb.currentText()

    def back(self):
        menu.show()
        self.hide()


class ShowObs(QWidget):
    def __init__(self, txt, d1, d2, area_name, obs, area, th, area_only):
        super(ShowObs, self).__init__()
        self.lista = None
        self.loc = None
        self.setWindowTitle('Prezentacja obserwacji')
        self.setWindowIcon(QIcon('data' + os.sep + 'icon.png'))
        self.resize(menu.screen_width, menu.screen_height - 100)
        self.move(0, 0)
        self.n = obs['total_results']
        th = 'Tak' * th + 'Nie' * ((th + 1) % 2)

        # back button
        back_btn = QPushButton()
        back_btn.setIcon(QIcon('data' + os.sep + 'back.jpg'))
        back_btn.clicked.connect(self.back)

        hbox_back = QHBoxLayout()
        hbox_back.addStretch(1)
        hbox_back.addWidget(back_btn)

        # map
        if area_only:
            try:
                loclat = mapping(area)['coordinates'][0][0][0][::-1]
            except:
                loclat = mapping(area)['coordinates'][0][0][::-1]
            zoom = 3
        else:
            loclat = (0, 0)
            zoom = 2
            area_name = 'Ziemia'
        self.mapa = folium.Map(#width=int(menu.screen_width * 0.6),
                               #height=int(menu.screen_height * 0.83),
                               location=loclat, zoom_start=zoom)
        if area_only:
            folium.GeoJson(area).add_to(self.mapa)
        folium.TileLayer('cartodbpositron').add_to(self.mapa)
        folium.TileLayer('Stamen Terrain').add_to(self.mapa)
        folium.LayerControl().add_to(self.mapa)
        folium.LatLngPopup().add_to(self.mapa)
        self.add_obs(obs, area_only, area)
        self.html = self.mapa._repr_html_()

        self.webEngineView = QWebEngineView()

        r = []
        for i in obs['results']:
            try:
                o = [i['taxon']['id']]
                r.append(i)
            except:
                pass
        if len(r) > 0:
            print(str(pprint(r)))

        self.webEngineView.setHtml(self.html)
        # self.webEngineView.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        hbox_map = QHBoxLayout()
        hbox_map.addWidget(self.webEngineView)
        #hbox_map.addWidget(self.lista)

        self.metric = QLabel(self)
        self.metric.setText(f'Obszar: {area_name}\nNazwa\Takson: {txt}\nData od: {d1} do: {d2}\nLiczba obserwacji: {self.n}\nTylko zagrożone: {th}')

        hbox = QHBoxLayout()
        hbox.addWidget(self.metric, 1)

        # layout settings
        vbox = QVBoxLayout()
        #vbox.addLayout(flo)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_map,1)
        #vbox.addWidget(self.webEngineView)
        vbox.addLayout(hbox_back)
        self.setLayout(vbox)

    def add_obs(self, obs, area_only, area):
        # A list
        #self.lista = QListWidget()
        #self.lista.sizeHint().setWidth(self.lista.sizeHintForColumn(0))

        for i in obs['results']:
            if i['geojson'] is not None:
                p = i['geojson']['coordinates']
                if (area_only and area.contains(Point(p))) or not area_only:
                    observation = Observation.from_json_list(i)[0]
                    label = ''#str(observation)
                    #self.lista.addItem(str(pprint(i)))
                    try:
                        #self.lista.addItem(str(i))
                        label = str(observation)
                        image = observation.photos[0].thumbnail_url
                        popup = my_plot_images([image], [label])
                    except:
                        popup = label
                    folium.Marker(p[::-1], popup=popup).add_to(self.mapa)
                else:
                    self.n -= 1
        self.n = max(self.n - 2, 0) if area_only else self.n

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
                folium.LatLngPopup().add_to(self.mapa)
                self.html = self.mapa._repr_html_()
                self.webEngineView.setHtml(self.html)
                print('obszar poprawnie skonstruowany')  # todo: error okno zapisać?

                # messagebox
                repply_msbox = QMessageBox.question(self, 'Poprawnie skonstruowano obszar',
                                                    'Obszar poprawnie skonstruowany.\nAby zapisać, kliknij \"Yes\".',
                                                    QMessageBox.Yes | QMessageBox.Cancel)
                if repply_msbox == QMessageBox.Yes:
                    self.loc = lista
                    self.save_area()

#menu.obs.generate_from_base..setEnabled(False)

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
