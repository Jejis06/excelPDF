# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel,QStackedWidget
import data_lib
import os
import sys

class Ui_Form(object):

    def __init__(self):
        self.files = None

    def load_settings(self):
        saved_data = data_lib.get_data(os.path.join(os.getcwd(), 'data.json'))
        if saved_data is None: return

        # file settings
        try:
            self.RangeStart.setText(str(saved_data['data_settings']['rangeStart']))
        except:
            None
        try:
            self.RangeEnd.setText(str(saved_data['data_settings']['rangeEnd']))
        except:
            None
        try:
            self.Plik.setText(str(saved_data['data_settings']['filename']))
        except:
            None

        # data settings
        try:
            self.Lokator.setText(str(saved_data['user_data_settings']['LOKATOR']))
        except:
            None
        try:
            self.LokalUrzytkowy.setText(str(saved_data['user_data_settings']['LOKAL_URZYTKOWY']))
        except:
            None
        try:
            self.ZuzycieWodyZimnej.setText(str(saved_data['user_data_settings']['ZUZYCIE_WODY_ZIMNEJ']))
        except:
            None
        try:
            self.ZuzycieWodyCieplej.setText(str(saved_data['user_data_settings']['ZUZYCIE_WODY_CIEPLEJ']))
        except:
            None
        try:
            self.StawkaWodaZimna.setText(str(saved_data['user_data_settings']['STAWKA_ZA_WODE_ZIMNA_I_SCIEKI']))
        except:
            None
        try:
            self.RozniceLicznikow.setText(
                str(saved_data['user_data_settings']['ROZNICE_LICZNIKOW_ORAZ_CZESCI_WSPOLNE']))
        except:
            None
        try:
            self.kosztStalyPodgrzanie.setText(str(saved_data['user_data_settings']['KOSZT_STALY_PODGRZANIA']))
        except:
            None
        try:
            self.StawkaPodgrzanie.setText(str(saved_data['user_data_settings']['STAWKA_ZA_PODGRZANIE_WODY']))
        except:
            None
        try:
            self.Mail.setText(str(saved_data['user_data_settings']['MAIL']))
        except:
            None
        try:
            self.Nabywca.setText(str(saved_data['user_data_settings']['NABYWCA']))
        except:
            None
        try:
            self.AdresKorespondencyjny.setText(str(saved_data['user_data_settings']['ADRES_KORESPONDENCYJNY']))
        except:
            None

        # mail settings
        try:
            self.RootMail.setText(str(saved_data['mail_settings']['ROOT_MAIL']))
        except:
            None
        try:
            self.Tytul.setText(str(saved_data['mail_settings']['SUBJECT']))
        except:
            None
        try:
            self.Tresc.setPlainText(str(saved_data['mail_settings']['CONTENT']))
        except:
            None
        try:
            self.Auth.setText(str(saved_data['mail_settings']['AUTH']))
        except:
            None
        try:
            self.RachunekBankowy.setText(str(saved_data['mail_settings']['RACHUNEK_BANKOWY']))
        except:
            None
        try:
            self.Sprzedawca.setPlainText(str(saved_data['mail_settings']['SPRZEDAWCA']))
        except:
            None

        return

    def get_settings(self):
        # mailbox settings
        doc_settings = {
            "data_settings": {
                "rangeStart": self.RangeStart.text(),
                "rangeEnd": self.RangeEnd.text(),
                "filename": self.Plik.text(),
            },

            "user_data_settings": {
                "LOKATOR": self.Lokator.text(),
                "LOKAL_URZYTKOWY": self.LokalUrzytkowy.text(),
                "ZUZYCIE_WODY_ZIMNEJ": self.ZuzycieWodyZimnej.text(),
                "ZUZYCIE_WODY_CIEPLEJ": self.ZuzycieWodyCieplej.text(),
                "STAWKA_ZA_WODE_ZIMNA_I_SCIEKI": self.StawkaWodaZimna.text(),
                "ROZNICE_LICZNIKOW_ORAZ_CZESCI_WSPOLNE": self.RozniceLicznikow.text(),
                "KOSZT_STALY_PODGRZANIA": self.kosztStalyPodgrzanie.text(),
                "STAWKA_ZA_PODGRZANIE_WODY": self.StawkaPodgrzanie.text(),
                "MAIL": self.Mail.text(),
                "ADRES_KORESPONDENCYJNY": self.AdresKorespondencyjny.text(),
                "NABYWCA": self.Nabywca.text(),

            },

            "mail_settings": {
                "ROOT_MAIL": self.RootMail.text(),
                "AUTH": self.Auth.text(),
                "SUBJECT": self.Tytul.text(),
                "CONTENT": self.Tresc.toPlainText(),
                "SPRZEDAWCA": self.Sprzedawca.toPlainText(),
                "RACHUNEK_BANKOWY": self.RachunekBankowy.text()
            }
        }
        return doc_settings

    def sendPdfAction(self):
        print("send pdf click")
        if self.files is None:
            self.OUT.appendPlainText("[YOU DIDNT GENERATE PDFS]")
            return
        self.OUT.appendPlainText("[SENDING PDFS.....]")
        with data_lib.Capturing() as output:
            data_lib.send_pdfs(self.files, self.RootMail.text(), self.Auth.text(), self.Tytul.text(),
                               self.Tresc.toPlainText())

        for out in output:
            self.OUT.appendPlainText(out)

        return

    def generatePdfAction(self):

        self.OUT.setPlainText("[GENERATING PDFS.....]")
        settings = self.get_settings()
        dane = data_lib.Data(settings)

        with data_lib.Capturing() as output:
            self.files = dane.generate_pdfs(self.PoczatekOkr.date().toPyDate().strftime("%d.%m.%Y"),
                                            self.KoniecOkr.date().toPyDate().strftime("%d.%m.%Y"))
        for out in output:
            self.OUT.appendPlainText(out)

        return

    def setupUi(self, Form, app):
        Form.setObjectName("Form")
        Form.resize(616, 687)
        font = QtGui.QFont()
        font.setFamily("Arial")
        Form.setFont(font)


        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 601, 418))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)


        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.Auth = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.Auth.setObjectName("Auth")
        self.horizontalLayout_7.addWidget(self.Auth)
        self.gridLayout.addLayout(self.horizontalLayout_7, 2, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_14 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_13.addWidget(self.label_14)

        self.StawkaWodaZimna = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.StawkaWodaZimna.setObjectName("StawkaWodaZimna")
        self.horizontalLayout_13.addWidget(self.StawkaWodaZimna)

        self.gridLayout_3.addLayout(self.horizontalLayout_13, 4, 0, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_11.addWidget(self.label_12)
        self.ZuzycieWodyZimnej = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.ZuzycieWodyZimnej.setObjectName("ZuzycieWodyZimnej")
        self.horizontalLayout_11.addWidget(self.ZuzycieWodyZimnej)
        self.gridLayout_3.addLayout(self.horizontalLayout_11, 2, 0, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_12.addWidget(self.label_13)
        self.ZuzycieWodyCieplej = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.ZuzycieWodyCieplej.setObjectName("ZuzycieWodyCieplej")
        self.horizontalLayout_12.addWidget(self.ZuzycieWodyCieplej)
        self.gridLayout_3.addLayout(self.horizontalLayout_12, 3, 0, 1, 1)

        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_9.addWidget(self.label_10)
        self.Lokator = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.Lokator.setObjectName("Lokator")
        self.horizontalLayout_9.addWidget(self.Lokator)
        self.gridLayout_3.addLayout(self.horizontalLayout_9, 0, 0, 1, 1)

        # NABYWCA --- ADD SAVING DATA
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_22 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_22.setFont(font)
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_20.addWidget(self.label_22)
        self.Nabywca = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.Nabywca.setObjectName("Nabywca")
        self.horizontalLayout_20.addWidget(self.Nabywca)
        self.gridLayout_3.addLayout(self.horizontalLayout_20, 9, 0, 1, 1)

        # ADRES KORESPONDENCYJNY --- ADD SAVING DATA
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_23 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_23.setFont(font)
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_21.addWidget(self.label_23)
        self.AdresKorespondencyjny = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.AdresKorespondencyjny.setObjectName("AdresKorespondencyjny")
        self.horizontalLayout_21.addWidget(self.AdresKorespondencyjny)
        self.gridLayout_3.addLayout(self.horizontalLayout_21, 10, 0, 1, 1)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.LokalUrzytkowy = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.LokalUrzytkowy.setObjectName("LokalUrzytkowy")
        self.horizontalLayout_2.addWidget(self.LokalUrzytkowy)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_15 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_14.addWidget(self.label_15)
        self.RozniceLicznikow = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.RozniceLicznikow.setObjectName("RozniceLicznikow")
        self.horizontalLayout_14.addWidget(self.RozniceLicznikow)
        self.gridLayout_3.addLayout(self.horizontalLayout_14, 5, 0, 1, 1)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_17 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_16.addWidget(self.label_17)
        self.StawkaPodgrzanie = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.StawkaPodgrzanie.setObjectName("StawkaPodgrzanie")
        self.horizontalLayout_16.addWidget(self.StawkaPodgrzanie)
        self.gridLayout_3.addLayout(self.horizontalLayout_16, 7, 0, 1, 1)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_16 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_15.addWidget(self.label_16)
        self.kosztStalyPodgrzanie = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.kosztStalyPodgrzanie.setObjectName("kosztStalyPodgrzanie")
        self.horizontalLayout_15.addWidget(self.kosztStalyPodgrzanie)
        self.gridLayout_3.addLayout(self.horizontalLayout_15, 6, 0, 1, 1)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_18 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_18.setFont(font)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_17.addWidget(self.label_18)
        self.Mail = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.Mail.setObjectName("Mail")
        self.horizontalLayout_17.addWidget(self.Mail)
        self.gridLayout_3.addLayout(self.horizontalLayout_17, 8, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 4, 2, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.RangeStart = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.RangeStart.setObjectName("RangeStart")
        self.horizontalLayout_6.addWidget(self.RangeStart)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.RangeEnd = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.RangeEnd.setObjectName("RangeEnd")
        self.horizontalLayout_5.addWidget(self.RangeEnd)
        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 2, 1, 1)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.Tresc = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.Tresc.setObjectName("Tresc")
        self.verticalLayout.addWidget(self.Tresc)

        # Sprzedawca ----- ADD SAVING DATA

        self.label_20 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_20.setFont(font)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.verticalLayout.addWidget(self.label_20)

        self.Sprzedawca = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.Sprzedawca.setObjectName("Sprzedawca")
        self.verticalLayout.addWidget(self.Sprzedawca)

        # Rachunek bankowy ------- ADD SAVING DATA
        self.label_21 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_21.setFont(font)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.verticalLayout.addWidget(self.label_21)

        self.RachunekBankowy = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.RachunekBankowy.setObjectName("RachunekBankowy")
        self.verticalLayout.addWidget(self.RachunekBankowy)

        self.gridLayout.addLayout(self.verticalLayout, 4, 0, 1, 1)

        # LOKAL USlugowy

        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_8.addWidget(self.label_9)
        self.Tytul = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.Tytul.setObjectName("Tytul")
        self.horizontalLayout_8.addWidget(self.Tytul)
        self.gridLayout.addLayout(self.horizontalLayout_8, 3, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.RootMail = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.RootMail.setObjectName("RootMail")
        self.horizontalLayout_4.addWidget(self.RootMail)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_19 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_19.setFont(font)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_18.addWidget(self.label_19)
        self.Plik = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.Plik.setObjectName("Plik")
        self.horizontalLayout_18.addWidget(self.Plik)
        self.gridLayout.addLayout(self.horizontalLayout_18, 2, 2, 1, 1)

        # pdf button generate
        self.GeneratePdf = QtWidgets.QPushButton(Form)
        self.GeneratePdf.setGeometry(QtCore.QRect(10, 460, 113, 32))
        self.GeneratePdf.setObjectName("GeneratePdf")
        self.GeneratePdf.clicked.connect(self.generatePdfAction)

        # pdf button send
        self.SendPdf = QtWidgets.QPushButton(Form)
        self.SendPdf.setGeometry(QtCore.QRect(120, 460, 113, 32))
        self.SendPdf.setObjectName("SendPdf")
        self.SendPdf.clicked.connect(self.sendPdfAction)

        # debug window to paste output into
        self.OUT = QtWidgets.QPlainTextEdit(Form)
        self.OUT.setGeometry(QtCore.QRect(10, 490, 601, 182))
        self.OUT.setObjectName("OUT")

        self.horizontalLayoutWidget_16 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_16.setGeometry(QtCore.QRect(10, 430, 469, 31))
        self.horizontalLayoutWidget_16.setObjectName("horizontalLayoutWidget_16")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_16)
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.NazwaPoczatek = QtWidgets.QLabel(self.horizontalLayoutWidget_16)
        self.NazwaPoczatek.setObjectName("NazwaPoczatek")
        self.horizontalLayout_19.addWidget(self.NazwaPoczatek)

        # poczatek okresu data
        self.PoczatekOkr = QtWidgets.QDateEdit(self.horizontalLayoutWidget_16)
        self.PoczatekOkr.setObjectName("PoczatekOkr")
        self.horizontalLayout_19.addWidget(self.PoczatekOkr)

        self.NazwaKoniec = QtWidgets.QLabel(self.horizontalLayoutWidget_16)
        self.NazwaKoniec.setObjectName("NazwaKoniec")
        self.horizontalLayout_19.addWidget(self.NazwaKoniec)

        # koniec okresu data
        self.KoniecOkr = QtWidgets.QDateEdit(self.horizontalLayoutWidget_16)
        self.KoniecOkr.setObjectName("KoniecOkr")
        self.horizontalLayout_19.addWidget(self.KoniecOkr)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ROZLICZENIA --- WODA"))
        self.label_7.setText(_translate("Form", "Auth"))
        self.label_14.setText(_translate("Form", "STAWKA ZA WODE ZIMNA I SCIEKI"))
        self.label_12.setText(_translate("Form", "ZUZYCIE WODY ZIMNEJ"))
        self.label_13.setText(_translate("Form", "ZUZYCIE WODY CIEPLEJ"))
        self.label_10.setText(_translate("Form", "LOKATOR"))
        self.label_3.setText(_translate("Form", "LOKAL URZYTKOWY"))
        self.label_15.setText(_translate("Form", "ROZNICE LICZNIKOW ORAZ CZESCI WSPOLNE"))
        self.label_17.setText(_translate("Form", "STAWKA ZA PODGRZANIE WODY"))
        self.label_16.setText(_translate("Form", "KOSZT STALY PODGRZANIA"))
        self.label_18.setText(_translate("Form", "MAIL"))
        self.label_6.setText(_translate("Form", "range start"))
        self.label_5.setText(_translate("Form", "range end"))
        self.label_8.setText(_translate("Form", "Mail content"))
        self.label_9.setText(_translate("Form", "Subject"))
        self.label_20.setText(_translate("Form", "Sprzedawca"))
        self.label_21.setText(_translate("Form", "Rachunek Bankowy"))
        self.label_22.setText(_translate("Form", "NABYWCA"))
        self.label_23.setText(_translate("Form", "ADRES KORESPONDENCYJNY"))
        self.label_4.setText(_translate("Form", "Email"))
        self.label.setText(_translate("Form", "Mailbox settings"))
        self.label_2.setText(_translate("Form", "Data settings"))
        self.label_19.setText(_translate("Form", "filepath"))
        self.GeneratePdf.setText(_translate("Form", "Generate PDFs"))
        self.SendPdf.setText(_translate("Form", "Send PDFs"))
        self.NazwaPoczatek.setText(_translate("Form", "Poczatek okresu rozl."))
        self.NazwaKoniec.setText(_translate("Form", "Koniec okresu rozl."))


