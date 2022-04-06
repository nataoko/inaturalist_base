from PyQt5.QtWidgets import *
import sys
from inaturalist import name_list
class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)
        #print(names)
        self.ledit_name = QLineEdit()

        names = []
        for i in map(str, name_list(self.ledit_name.text())):
            name = i.split(': ')[1].split(' ', 1)[0]

            print(name.lower(), i)
            names.append(name.lower())
        self.ledit_name.setCompleter(QCompleter(names))
        layout.addWidget(self.ledit_name, 1, 0)
        # auto complete options                                                 
        names = ["Apple", "Alps", "Berry", "Cherry" ]
        completer = QCompleter(names)

        # create line edit and add auto complete                                
        self.lineedit = QLineEdit()
        self.lineedit.setCompleter(completer)
        layout.addWidget(self.lineedit, 0, 0)

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())