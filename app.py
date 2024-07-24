# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import openpyxl
import os
import json
import base_doc
import pdfkit

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
        "MAIL": "U",
    }
}

def html_to_pdf(html_content, output_path, user):
    pdfkit.from_string(html_content, output_path)
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
            if (key == 'LOKAL_URZYTKOWY'): continue
            if user[key] is None: user[key] = 0

        users[user["LOKATOR"]] = user

    #print(json.dumps(users, indent=4))
    return users


users = load_data()
for user in users.keys():
    raw_html = base_doc.get_form_for_user(users[user])
    try:
        html_to_pdf(raw_html, os.path.join(os.path.join(os.getcwd(), 'pdfs'), str(user + ".pdf")), user)
        print(f"Successfully converted html to pdf | {user} | {users[user]['MAIL']}")
    except Exception as e:
        print(f"Failed to convert html to pdf: {e} | {user} | {users[user]['MAIL']}")
