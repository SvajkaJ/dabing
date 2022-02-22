#!/usr/bin/python3
# Autor: SvajkaJ
# Date:  19.8.2021

import subprocess

def _check_process(process, label):
    p = subprocess.Popen(f"ps fx | grep \"{process}\"", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].splitlines()
    if len(data) < 3:
        return { "label": label, "active": False }
    else:
        return { "label": label, "active": True }

def _check_usb(process, label):
    p = subprocess.Popen(f"lsusb | grep \"{process}\"", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].splitlines()
    if len(data) < 1:
        return { "label": label, "active": False }
    else:
        return { "label": label, "active": True }

def get_status_info():
    statusInfo = []
    statusInfo.append(_check_process("SNMP_SERVER.py", "SNMP Server"))
    statusInfo.append(_check_process("welle-cli", "welle-cli"))
    statusInfo.append(_check_usb("RTL2838 DVB-T", "RTL-SDR RTL2838"))
    return { "statusInfo": statusInfo }

if __name__ == "__main__":
    print(_check_usb("RTL2838 DVB-T", "RTL-SDR RTL2838"))
