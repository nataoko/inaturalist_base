from PyQt5.QtWidgets import QApplication,QLineEdit,QWidget,QFormLayout, QPushButton
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from PyQt5.QtCore import Qt
import sys


def main():

    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())




class lineEditDemo(QWidget):
        def __init__(self,parent=None):
                super().__init__(parent)
                e1 = QLineEdit()
                e1.setValidator(QIntValidator())
                e1.setMaxLength(4)
                e1.setAlignment(Qt.AlignRight)
                e1.setFont(QFont("Arial",20))

                e2 = QLineEdit()
                e2.setValidator(QDoubleValidator(0.99,99.99,5))
                e3 = QLineEdit()
                e3.setInputMask("+99_9999_999999")

                e4 = QLineEdit()
                e4.textChanged.connect(self.textchanged)

                self.e44 = QLineEdit()
                self.e44.textChanged.connect(self.textchanged)
                
                e4.textChanged.connect(self.textchanged)
                e5 = QLineEdit()
                e5.setEchoMode(QLineEdit.Password)

                e6 = QLineEdit("Hello PyQt5")
                e6.setReadOnly(True)
                e5.editingFinished.connect(self.enterPress)

                flo = QFormLayout()
                flo.addRow("Obszar: Park Krajobrazory A Liczba obserwacji: 109",e4)
                flo.addRow("Data od: 12-10-2021 do: 30-12-2021 Taxon: 12121",self.e44)

##                flo.addRow("Data od",e4)
##                flo.addRow("Data do",e4)
##                flo.addRow("integer validator",e1)
##                flo.addRow("Double validator",e2)
##                flo.addRow("Input Mask",e3)
##                flo.addRow("Nazwa obszaru",e4)
##                flo.addRow("Password",e5)
##                flo.addRow("Read Only",e6)

                self.setLayout(flo)
                self.setWindowTitle("Obserwacje")

        def textchanged(self,text):
                print("Changed: " + text+self.e44.text())
                self.e44.setEchoMode

        def enterPress(self):
                print("Enter pressed")

if __name__ == "__main__":
        app = QApplication(sys.argv)
        win = lineEditDemo()
        win.show()
        sys.exit(app.exec_())
