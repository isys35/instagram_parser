from PyQt5 import QtGui, QtWidgets
import mainwindow
import sys
from logic import InstaParser


class MainApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.auth)
        self.pushButton_2.clicked.connect(self.find_locations)
        self.parser = InstaParser()

    def auth(self):
        self.parser.auth(self.lineEdit.text(), self.lineEdit_2.text())
        if self.parser.agent:
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.pushButton.setEnabled(False)
            print('[INFO] Авторизация успешна')

    def find_locations(self):
        if self.parser.agent:
            self.parser.find_locations(self.lineEdit_3.text())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
