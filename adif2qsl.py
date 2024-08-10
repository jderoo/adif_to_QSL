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
import csv
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
    logfilename = config['general']['logfilename']
    log = adif_io.read_from_file(logfilename)
except:
    exit("Error: Can't open logfile") 

print(f"After logfile read")

with open(config['general']['keysfilename'],newline='') as keysfile:
    reader = csv.reader(keysfile)
    for row in reader:
        keys = row

# allocate the data storage
qso_data = []
# iterate through the qsos
for row_num, qso in enumerate(log[0]):
    # Calculate YEAR, MONTH, DAY, HOUR, an MINUTE from the dain-bramaged
    # format used by ADIF
    qso['YEAR']=qso['QSO_DATE'][0:4]
    qso['MONTH']=qso['QSO_DATE'][4:6]
    qso['DAY']=qso['QSO_DATE'][6:8]
    qso['HOUR']=qso['TIME_ON'][0:2]
    qso['MINUTE']=qso['TIME_ON'][2:4]
    
    qso_row = []
    
    # iterate through the keys
    for col_num, key in enumerate(keys):
        if key in qso:
            qso_row.append(qso[key])
        else:
            qso_row.append('')
    qso_data.append(qso_row)

with open(config['general']['csvfilename'],'w',newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(keys)
    writer.writerows(qso_data)
