from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread
import mainwindow
import sys
from logic import InstaParser
import traceback


class MainApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.auth)
        self.pushButton_2.clicked.connect(self.find_locations)
        self.pushButton_3.clicked.connect(self.get_data)
        self.parser = InstaParser()
        self.locations = None
        self.threadparser = None

    def auth(self):
        self.parser.auth(self.lineEdit.text(), self.lineEdit_2.text())
        if self.parser.agent:
            self.label.setEnabled(False)
            self.label_2.setEnabled(False)
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
            min_folowers = int(self.lineEdit_3.text())
            self.threadparser = ThreadGetData(self, index, min_folowers)
            self.threadparser.start()
            self.lineEdit_3.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.lineEdit_4.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.comboBox.setEnabled(False)
            self.label_3.setEnabled(False)
            self.label_4.setEnabled(False)
            self.label_5.setEnabled(False)


class ThreadGetData(QThread):
    def __init__(self, window, index, min_folowers):
        super().__init__()
        self.min_folowers = min_folowers
        self.window = window
        self.index = index

    def run(self):
        try:
            self.parser.window = self.window
            self.window.parser.min_folowers_locations = self.min_folowers
            self.window.parser.get_data(self.index)
        except Exception as ex:
            print(ex)
            print(traceback.format_exc())



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
