from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_email_pdf_figs(path_to_pdf, subject, message, destination, mail, password, pdf_filename):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(mail, password)
    msg = MIMEMultipart()

    message = f'{message}'
    msg['Subject'] = subject
    msg['From'] = mail
    msg['To'] = destination

    # Insert the text to the msg going by e-mail
    msg.attach(MIMEText(message, "plain"))

    # Attach the pdf to the msg going by e-mail
    with open(path_to_pdf, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
    attach.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
    msg.attach(attach)

    # send msg
    server.send_message(msg)
