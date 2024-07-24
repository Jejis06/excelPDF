# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import openpyxl
import os
import json

doc_settings = {
    "data_settings": {
        "rangeStart": "A5",
        "rangeEnd": "U28",
        "filename": "Woda062024.xlsx",
    },

    "user_data_settings": {
        "LOKATOR": "A",
        "LOKAL_URZYTKOWY": "B",
        "ZUZYCIE_WODY_ZIMNEJ": "G",
        "ZUZYCIE_WODY_CIEPLEJ": "J",
        "STAWKA_ZA_WODE_ZIMNA_I_SCIEKI": "L",
        "ROZNICE_LICZNIKOW_ORAZ_CZESCI_WSPOLNE": "N",
        "KOSZT_STALY_PODGRZANIA": "P",
        "STAWKA_ZA_PODGRZANIE_WODY": "Q",
    }
}


def get_col(cell: str, row: any):
    return row[ord(cell) - ord('A')]


def load_data(settings=None):
    if settings is None:
        settings = doc_settings
    users = {}

    filename = settings['data_settings']['filename']
    rangeStart = settings['data_settings']['rangeStart']
    rangeEnd = settings['data_settings']['rangeEnd']

    path = os.path.join(os.getcwd(), filename)

    workbook = openpyxl.load_workbook(path)
    sheetNames = workbook.sheetnames
    sheet = workbook[sheetNames[0]]

    rows = sheet[rangeStart + ":" + rangeEnd]
    for row in rows:
        user = {}
        for key, val in settings['user_data_settings'].items():
            user[key] = get_col(val, row).value
        users[user["LOKATOR"]] = user

    print(json.dumps(users, indent=4))
    return users


load_data()
