import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout

if __name__ == '__main__':    
    app = QApplication(sys.argv)
    w = QWidget()    
    layout = QHBoxLayout()
    btn = QPushButton("Nowy obszar Obserwacje O Aplikacji")
    layout.addWidget(btn)
    w.setLayout(layout)
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Menu')
    w.show()
    sys.exit(app.exec_())

##Park Krajobrazowy A 01-03-2021 30-11-2021 12231
##Park Krajobrazowy A 01-03-2021 30-11-2021 12323
##Park Krajobrazowy A 01-03-2021 30-11-2021 11233
##Park Krajobrazowy A 01-03-2021 30-11-2021 12444
##Park Krajobrazowy B 01-03-2021 30-11-2021 11233
##Park Krajobrazowy B 01-03-2021 30-11-2021 12444
##Polska 01-03-2021 30-11-2021 11233
##Europa A 01-03-2021 30-11-2021 12444
