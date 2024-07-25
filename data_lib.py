# -*- coding: utf-8 -*-
import openpyxl
import os
import base_doc
import pdfkit
import json
import mail_module
from io import StringIO
import sys

def get_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        f.close()
    return data
def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)
        f.close()


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
def send_pdfs(files, mail, auth, subject, message):
    for file in files:
        try:
            mail_module.send_email_pdf_figs(file["pdf_path"], subject, message, file['mail'], mail, auth)
            print(f"Succesfully sent email to {file['mail']}/{file['user']}")
        except Exception as e:
            print(f"Could not send email to {file['mail']}/{file['user']} {e}")


class Data:
    def __init__(self, settings):
        self.reload_settings(settings)
        self.pdfs_path = "pdfs"
        return

    def reload_settings(self, settings):
        self.doc_settings = settings
        self.users = self.load_data()
        return

    def html_to_pdf(self, html_content: str, output_path: os.path, user):
        pdfkit.from_string(html_content, output_path)

    def get_col(self, cell: str, row: any):
        return row[ord(cell) - ord('A')]

    def load_data(self, settings=None):
        if settings is None:
            settings = self.doc_settings
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
                user[key] = self.get_col(val, row).value
                if (key == 'LOKAL_URZYTKOWY'): continue
                if user[key] is None: user[key] = 0

            users[user["LOKATOR"]] = user

        return users

    # returns list of objects with usernames, mails, and path to pdf
    def generate_pdfs(self, okres1, okres2):
        users = self.users
        if os.path.exists(os.path.join(os.getcwd(), self.pdfs_path)) is False:
            os.mkdir(os.path.join(os.getcwd(), self.pdfs_path))
        res = []

        for user in users.keys():
            raw_html = base_doc.get_form_for_user(users[user], okres1, okres2)
            try:
                user_path = os.path.join(os.getcwd(), self.pdfs_path, str(user) + ".pdf")
                self.html_to_pdf(raw_html, user_path, user)
                print(f"Successfully converted html to pdf | {user} | {users[user]['MAIL']}")

                user_mail = {
                    "user": user,
                    "mail": users[user]["MAIL"],
                    "pdf_path": user_path
                }
                res.append(user_mail)

            except Exception as e:
                print(f"Failed to convert html to pdf: {e} | {user} | {users[user]['MAIL']}")

        if len(res) == 0:
            raise Exception("No emails generated due to above errors")
        return res

