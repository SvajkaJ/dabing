# About
My Master's thesis: Monitoring device of DAB+ broadcasting.

This work is using Welle.io under the hood. I would like to thank the developers of Welle.io for creating, maintaining and sharing this wonderful application.

# Installing
Instalation manual is in my thesis as an attachment.

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
pip3 install pysnmp flask flask-cors uptime uwsgi
pip3 install psycopg2                                  // python adapter for postgres
```

<!--
pip3 install uptime
sudo apt install -y net-tools build-essential file
sudo apt install -y nodejs npm

sudo apt-get install -y postgresql-contrib
-->

# Known bugs and limitations
## pysnmp
Library is no longer maintained!
* **Directory:** "/home/pi/.local/lib/....../site-packages/pysnmp/smi"
* **File:** "rft1902.py"
* **Line:** around 306 or 320
* **Correct:** "def resolveWithMib(self, mibViewController, ignoreErrors=True):"

Patch should be somewhere available!
