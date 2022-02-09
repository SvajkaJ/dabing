<img src="./logo.svg" width="300" alt="DABIng+">

# About
This work is primarily focused on monitoring quality of DAB+ transmission. The parameters which are monitored mainly are Bit Error Rate (BER), Signal To Noise Ratio (SNR), Fast Information Block Error Rate (FIBER*), Bandwidth, etc. This work is using Welle.io under the hood because most of the basic funcionality such as decoding DAB+ signal are already in place. Overall, Welle.io is a really good application which I would like to thank the developers for creating and sharing under GPL license.
\* Relative error rate of faulty Cyclic Redundancy Check (CRC)s.

Needed npm packages for web: (For now not relevant)
* @fortawesome/fontawesome-svg-core // not used so far
* @fortawesome/free-solid-svg-icons // not used so far
* @fortawesome/react-fontawesome // not used so far
* react-router-dom // not used so far
* node-sass
* @blueprintjs/core
* @blueprintjs/popover2
* @blueprintjs/select

# Raspi-config
* enable ssh
* enable 1-Wire
* enable I2C
* set Location


# Installing
Update your system. This step is optional when you have updated your system in the recent past.
```
sudo apt update
```

Installed so far:
```
sudo apt install -y python3 python3-pip git
sudo apt install -y postgresql
```

#sudo apt install -y net-tools build-essential file
#sudo apt install -y nodejs npm
#sudo apt install nginx
#sudo apt-get install -y postgresql-contrib


NPM packages used in this project:
* @blueprintjs/core 
* @nivo/core
* @nivo/line
* @blueprintjs/popover2
* @blueprintjs/select


# pysnmp library has a bug
Directory: "/home/pi/.local/lib/....../site-packages/pysnmp/smi"
File: "rft1902.py"
Line: around 306 or 320
Correct: "def resolveWithMib(self, mibViewController, ignoreErrors=True):"
Patch should be somewhere available
