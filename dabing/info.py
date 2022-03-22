#!/usr/bin/python3
# Autor: SvajkaJ
# Date:  28.2.2022

import subprocess

def get_HW():
    """Hardware."""
    p = subprocess.Popen("cat /proc/cpuinfo | grep 'model name\|Model'", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].splitlines()
    return (data[-1][9:] + data[0][12:])

def get_SW():
    """Software."""
    p = subprocess.Popen("cat /proc/version", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].split()
    return " ".join(data[:3])

def get_NW():
    """Network."""
    p = subprocess.Popen("lsusb -t | grep Vendor | cut -f 1 -d ',' | cut -f 2 -d 'v'", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].strip()
    p = subprocess.Popen("lsusb | grep 'Device 00" + data + "' | cut -f 3 -d ':' | cut -f 2- -d ' '", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    data = p.communicate()[0].strip()
    return data

def get_HN():
    """Hostname."""
    p = subprocess.Popen("hostname", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    result = p.communicate()[0].strip()
    return result

def get_device_info():
    return {
        "hardware": get_HW(),
        "software": get_SW(),
        "network":  get_NW(),
        "hostname": get_HN()
    }

if __name__ == "__main__":
    print(get_device_info())
