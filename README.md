### adif_to_QSL

Quick Python script to:

* Parse an ADIF log file.
* Generate a CSV of specified fields that can be read in by MS Publisher

To make it work, 

1. cp config.template config

2. Edit config and update the fields in the [email] and [qrz] sections.

3. cp keys.csv.template keys.csv

4. Edit keys.csv to specify the ADIF keys you want transferred to the CSV

5. Install the adif_io lib

   `pip3 install -r requirements.txt`

6. Place your ADIF log in the same folder and call it `log.adi` (the
   log.adi.template that is already there is just a few headers and no
   content)

7. Run the program.
   `python3 adif2qsl.py`

### TODO ###
  * Handle non-existant frequencies or ones with too many significant
    figures
  * Combine adif reader and CSV writer functionality so the whole thing
    doesn't have to be stored
  * Think about adding mechanism to have additional info (e.g.,
    portable/mobile operation checkboxes & location, qsl-pse and qsl-tnx
    check boxes or circles), and QSL-specific comments
  * Think about resurrecting the print-data-in-specific-positions
    functionality to print data on pre-printed QSL cards.  Might be
    easier to use MS Publisher to handle the positioning, but this way
    might allow more programmatic control.
  * Keep looking for better way into MS Publisher - csv is non-optimal
