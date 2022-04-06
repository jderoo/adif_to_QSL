#!/usr/bin/env python3

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from PIL import Image, ImageDraw, ImageFont
import adif_io
from lookup import QRZlookup

my_email_address = "mbridak@sergio"  # your from email address

mailserver = "smtp.gmail.com"

email_text = "Thanks for the QSO, 73, Mike K6GTE."  # message body

qrz = QRZlookup("AC4LL", "Secret")  # enter your userid and password

log = adif_io.read_from_file("./log.adi")


def send_mail(send_from, send_to, subject, text, files=None, server="127.0.0.1"):
    """its a doc string..."""
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg["From"] = send_from
    msg["To"] = COMMASPACE.join(send_to)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        # After the file is closed
        part["Content-Disposition"] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    try:
        smtp = smtplib.SMTP(server, 587)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
    except smtplib.SMTPException as err:
        print(f"Whoops! SMTP error - {err}")


for record in log[0]:
    grid, name, nickname, email, error_text = qrz.lookup(record["CALL"])
    time_utc = f"{record['TIME_ON'][0:2]}:{record['TIME_ON'][2:4]}"
    freq_band = None
    if "FREQ" in record:
        freq_band = "{:.3f}".format(float(record["FREQ"]))
    else:
        freq_band = record["BAND"]

    the_date = (
        f"{record['QSO_DATE'][0:4]}-{record['QSO_DATE'][4:6]}-{record['QSO_DATE'][6:8]}"
    )
    print(
        f"{record['CALL']} {record['MODE']} {freq_band} {record['BAND']} {time_utc} {record['RST_SENT']} {record['RST_RCVD']} {email} {error_text}"
    )
    print(record)

    img = Image.open("qslcard.png")
    working_image = ImageDraw.Draw(img)
    Font = ImageFont.truetype("./JetBrainsMono-Regular.ttf", 24)
    smFont = ImageFont.truetype("./JetBrainsMono-Regular.ttf", 14)
    working_image.text(
        (55, 331), record["CALL"], font=Font, anchor="ms", fill=(0, 0, 0)
    )
    working_image.text((120, 305), the_date, font=smFont, fill=(0, 0, 0))
    working_image.text((140, 320), time_utc, font=smFont, fill=(0, 0, 0))
    working_image.text((266, 331), freq_band, font=Font, anchor="ms", fill=(0, 0, 0))
    working_image.text(
        (372, 331), record["MODE"], font=Font, anchor="ms", fill=(0, 0, 0)
    )
    working_image.text(
        (430, 305), " SENT: " + record["RST_SENT"], font=smFont, fill=(0, 0, 0)
    )
    working_image.text(
        (430, 320), " RCVD: " + record["RST_RCVD"], font=smFont, fill=(0, 0, 0)
    )
    img.save("QSL_CARD.png")
    send_mail(
        my_email_address,
        [
            email,
        ],
        f"Our QSO on {the_date}",
        email_text,
        [
            "QSL_CARD.png",
        ],
        mailserver,
    )
