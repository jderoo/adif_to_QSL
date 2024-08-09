#!/usr/bin/env python3
"""
Takes an adif log 'log.adi' from the local directory,
looks up the callsign on QRZ. Gets the email address.
Fills out the card with adif info.
Emails card to contact.
"""

# Who's at fault_____: Mike K6GTE
# Where to yell at me: michael.bridak@gmail.com

import configparser
import smtplib
from os.path import basename
from os.path import isfile
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from PIL import Image, ImageDraw, ImageFont
import adif_io
from lookup import QRZlookup

config = configparser.ConfigParser()

try:
    isfile('config')
    config.read('config')
except:
    exit("Error: Unable to open or read config")

try:
    my_email_address = config['email']['my_email_address']
    mailserver       = config['email']['mailserver']
    username         = config['email']['username']
    password         = config['email']['password']
    email_text       = config['email']['text']
except:
    exit("Error: Missing at least one email configuration")

try:
    qrz = QRZlookup(config['qrz']['userid'], config['qrz']['password'])
except:
    exit("Error: QRZlookup initialization failure")

try:
    logfilename = config['general']['defaultlogfilename']
    log = adif_io.read_from_file(logfilename)
except:
    exit("Error: Can't open logfile") 

print(f"After logfile read")

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
        part["Content-Disposition"] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL(server, 465)
        server.ehlo()
        server.login(username, password)
        server.sendmail(send_from, send_to, msg.as_string())
        server.close()
    except smtplib.SMTPException as err:
        exit("Whoops! SMTP error - {err}")


for record in log[0]:
    grid, name, nickname, email, error_text = qrz.lookup(record["CALL"])
    time_utc = f"{record['TIME_ON'][0:2]}:{record['TIME_ON'][2:4]}"

    freq_band = None
    if "BAND" in record:
        freq_band = record["BAND"]
    else:
        freq_band = "{:.3f}".format(float(record["FREQ"]))

    the_date = (
        f"{record['QSO_DATE'][0:4]}-{record['QSO_DATE'][4:6]}-{record['QSO_DATE'][6:8]}"
    )
    print(
        f"{record['CALL']} {record['MODE']} {freq_band} {record['BAND']} "
        f"{time_utc} {record['RST_SENT']} {record['RST_RCVD']} {email}"
    )

    img = Image.open("qslcard.png")
    working_image = ImageDraw.Draw(img)
    Font = ImageFont.truetype("./JetBrainsMono-Regular.ttf", 24)
    smFont = ImageFont.truetype("./JetBrainsMono-Regular.ttf", 14)
    #
    # This section places the text on the card.
    # The first group  of numbers is the offset in pixels from upper left 0,0
    # Normal text anchor point is upper left of text.
    # lines with anchor='ms' places the anchor point in the middle of the text.
    #
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
    if email:
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
