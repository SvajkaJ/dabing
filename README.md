# About
My Master's thesis is primarily focused on monitoring quality parameters of DAB+ transmission. The parameters which are monitored are mainly Bit Error Rate (BER), Signal to Noise Ratio (SNR) and Power Spectrum Density (PSD).

This work is using Welle.io under the hood because most of the basic funcionality such as decoding DAB+ signal are already in place. I would like to thank the developers of Welle.io for creating, maintaining and sharing this wonderful application.

# Installing
Instalation manual is in my thesis as an attachment.

List of installed packages:
```
sudo apt install -y python3 python3-pip git
sudo apt install -y postgresql
sudo apt install -y rtl-sdr cmake
pip3 install pysnmp uptime Flask
```

<!--
sudo apt install -y net-tools build-essential file
sudo apt install -y nodejs npm
sudo apt install nginx
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
