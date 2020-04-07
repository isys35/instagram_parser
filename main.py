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
        self.pushButton_3.clicked.connect(self.get_data)
        self.parser = InstaParser()
        self.locations = None

    def auth(self):
        self.parser.auth(self.lineEdit.text(), self.lineEdit_2.text())
        if self.parser.agent:
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.pushButton.setEnabled(False)
            print('[INFO] Авторизация успешна')

    def find_locations(self):
        if self.parser.agent:
            self.locations = self.parser.find_locations(self.lineEdit_3.text())
            self.label_3.setText('Найдено локаций: ' + str(len(self.locations)))
            self.comboBox.clear()
            self.comboBox.addItems(self.locations)

    def get_data(self):
        if self.parser.agent:
            index = self.locations[self.comboBox.currentText()]
            self.parser.get_data(index)




def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
