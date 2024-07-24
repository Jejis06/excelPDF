import tkinter as tk
from tkinter import ttk
import openpyxl


def load_data():
    path = "C:\\Users\\ignac\\EXCELVIEWER\\dlugi.xlsx"
    rangeStart = "A1"
    rangeEnd = "C15"

    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active



    data = sheet[rangeStart + ":" + rangeEnd]

    for row in data:
        for cell in row:
            print(cell.value, end=' ')
        print()

load_data()