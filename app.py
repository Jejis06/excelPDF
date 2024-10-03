# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel,QStackedWidget
import data_lib
import os
import sys
from electricPage import Ui_Form2
from waterPage import Ui_Form



if __name__ == "__main__":
    # app passwords
    app = QtWidgets.QApplication(sys.argv)

    Woda = QtWidgets.QWidget()
    Prad = QtWidgets.QWidget()

    ui1 = Ui_Form()
    ui1.setupUi(Woda, app)
    ui1.load_settings()

    ui2 = Ui_Form2()
    ui2.setupUi(Prad, app)
    ui2.load_settings()


    Prad.show()
    Woda.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        data_lib.save_data('data.json', ui1.get_settings())
        data_lib.save_data('data2.json', ui2.get_settings())
