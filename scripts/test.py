from PyQt5.QtWidgets import QApplication, QWidget, \
     QPushButton, QLineEdit, QFormLayout,\
     QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
import folium
import io
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys

class PushButton(QWidget):
    def __init__(self):
        super(PushButton,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PushButton")
        self.setGeometry(400,400,300,260)
        self.closeButton = QPushButton(self)
        '''self.closeButton.setText("Close")          #text
        self.closeButton.setIcon(QIcon("close.png")) #icon
        self.closeButton.setShortcut('Ctrl+D')  #shortcut key
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setToolTip("Close the widget") #Tool tip
        self.closeButton.move(100,100)

        
'''

        m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
        w = QWebEngineView()
        w.setHtml(m.get_root().render())
    
        lineName = QLineEdit()
        #lineName.setMinLength(1)
        #lineName.setAlignment(Qt.AlignRight)
        #lineName.setFont(QFont("Arial",20))
        
        flo = QFormLayout()
        flo.addRow("Nazwa obszaru",lineName)

        self.setLayout(flo)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PushButton()
    ex.show()
    sys.exit(app.exec_()) 
