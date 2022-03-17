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

def get_status_info(config: dict):
    si = []
    ps = check_process("SNMP_SERVER.py")
    si.append({
        "label": "SNMP Server",
        "isOn": ps,
        "isOk": ps == True
    })
    ps = check_process("welle-cli")
    si.append({
        "label": "welle-cli",
        "isOn": ps,
        "isOk": ps == True
    })
    ps = check_usb("RTL2838 DVB-T")
    si.append({
        "label": "RTL-SDR RTL2838",
        "isOn": ps,
        "isOk": ps == True
    })
    ps = check_process("EVALUATION.py")
    si.append({
        "label": "EVALUATION",
        "isOn": ps,
        "isOk": ps == config["trapEnabled"]
    })
    return si

if __name__ == "__main__":
    print("SNMP Server:", check_process("SNMP_SERVER.py"))
    print("welle-cli:", check_process("welle-cli"))
    print("RTL-SDR RTL2838:", check_usb("RTL2838 DVB-T"))
    print("EVALUATION:", check_process("EVALUATION.py"))
