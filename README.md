### adif_to_QSL

Quick Python script to:

* Parse an ADIF log file.
* Get the email address of the radio contact.
* Generate a CSV of specified fields that can be read in by MS Publisher

To make it work, 

1. cp config.template config

2. Edit config and update the fields in the [email] and [qrz] sections.

3. Install the adif_io lib

   `pip3 install -r requirements.txt`

4. Place your ADIF log in the same folder and call it `log.adi` (the
   log.adi.template that is already there is just a few headers and no
   content)

5. Run the program.
   `python3 adif2qsl.py`

6. Oh very important, Change the QSL card graphic or you'll confuse people
   when they get My QSL card but for your contact...

You may want to check with your email provider for rate limits.
