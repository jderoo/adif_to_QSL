### adif_to_QSL

Quick Python script to:

* Parse an ADIF log file.
* Generate a QSL card populated with the specifics of the QSO.
* Get the email address of the radio contact.
* Email that user a copy of the QSL card as an attachment.

To make it work, change the following:

```
my_email_address = "youremail@address.com"

mailserver = "smtp.gmail.com"  # your mail server

username = my_email_address  # may or maynot be same as email addr.

password = "secretpassword"

email_text = "Thanks for the QSO, 73, Mike K6GTE."  # message body

qrz = QRZlookup("AC4LL", "secretpassword")  # enter your userid and password
```

Install the adif_io lib

`pip3 install -r requirements.txt`

Place your ADIF log in the same folder and call it `log.adi`

Run the program.

Oh very important, Change the QSL card graphic or you'll confuse people when they get My QSL card but for your contact...

You may want to check with your email provider for rate limits.
