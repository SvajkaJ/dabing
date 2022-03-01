#!/usr/bin/python3
# Autor: SvajkaJ
# Date:  28.2.2022

import subprocess

def check_process(process):
    p = subprocess.Popen(f"ps fx | grep \"{process}\"", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].splitlines()
    if len(data) < 3:
        return False
    else:
        return True

def check_usb(process):
    p = subprocess.Popen(f"lsusb | grep \"{process}\"", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].splitlines()
    if len(data) < 1:
        return False
    else:
        return True

def get_status_info():
    statusInfo = []
    statusInfo.append({ "label": "SNMP Server",     "active": check_process("SNMP_SERVER.py") })
    statusInfo.append({ "label": "welle-cli",       "active": check_process("welle-cli") })
    statusInfo.append({ "label": "RTL-SDR RTL2838", "active": check_usb("RTL2838 DVB-T") })
    return { "statusInfo": statusInfo }

if __name__ == "__main__":
    print("RTL-SDR RTL2838:", check_usb("RTL2838 DVB-T"))
