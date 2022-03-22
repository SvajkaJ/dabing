# About
**My Master's thesis:** Monitoring device of DAB+ broadcasting.

**Abstract:** The aim of this thesis is to build a monitoring device of the DAB+ broadcasting on the principle of SDR. The quality parameters of the DAB+ broadcasting examined in this thesis are RF input level, SNR, BER and FIBER. Monitoring device presented in this thesis deals with RTL2832U and Raspberry Pi microcomputer. Observing and managing the presented monitoring device is possible via the web interface, namely, HTTP and SNMP protocols. The important parts of the software used in this thesis are also presented.

This work is using Welle.io under the hood. I would like to thank the developers of Welle.io for creating, maintaining and sharing this wonderful application.

# Installing
Make sure that the project folder is in the */home/pi/* directory. In order to install this project, start *setup.sh* script in the *install* directory.

More detailed instalation manual is in my thesis as an attachment.

List of installed packages:
```
sudo apt install -y python3 python3-pip git
sudo apt install -y postgresql postgresql-server-dev-all
sudo apt install -y rtl-sdr cmake
sudo apt install -y libfftw3-dev librtlsdr-dev libfaad-dev libmp3lame-dev libmpg123-dev
sudo apt install -y libpq-dev libpqxx-dev              // c/c++ adapter for postgres
sudo apt install -y alsa-utils                         // should be already installed
sudo apt install -y libasound2-dev lame                // for alsa support in welle.io
sudo apt install -y nginx
pip3 install pysnmp flask flask-cors flask-expects-json uptime uwsgi
pip3 install psycopg2                                  // python adapter for postgres
```

<!--
I don't know if this is needed!
sudo apt install -y net-tools build-essential file postgresql-contrib
-->

# Usage
Read *user's manual* at the device's webpage in the *documentation* tab. Alternativelly, read my thesis.

# Known bugs and limitations
## [pysnmp](https://github.com/etingof/pysnmp)
Library *pysnmp* is no longer maintained!
* **Directory:** "/home/pi/.local/lib/....../site-packages/pysnmp/smi"
* **File:** "rft1902.py"
* **Line:** around 306 or 320
* **Correct:** "def resolveWithMib(self, mibViewController, ignoreErrors=True):"

Patch is applied during the installation process automatically.

## database
Regular data deletion is not being done. If you plan to use this project for a long peiod of time,
write your own program for deleting the data in the database to avoid filling up all available memory.

## TII
Transmitter Identification Information block may show incorrect data. It is the result of the implementation of the welle.io (tii-decoder). If you need this information to be precise, it is neccessary to change the implementation of the tii-decoder in welle.io.

## Response time
Generally speaking, Raspberry Pi may be busy and cannot respond to the HTTP request fast enough (sometimes not at all).

# License
This project is made available under the MIT License.
