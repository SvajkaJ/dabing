#!/usr/bin/python3
# Autor: SvajkaJ
# Datum: 27.2.2022


import json
import os
import subprocess


DABchannels = {
    # Band III
    174928000:  "5A",176640000:  "5B",178352000:  "5C",180064000:  "5D",
    181936000:  "6A",183648000:  "6B",185360000:  "6C",187072000:  "6D",
    188928000:  "7A",190640000:  "7B",192352000:  "7C",194064000:  "7D",
    195936000:  "8A",197648000:  "8B",199360000:  "8C",201072000:  "8D",
    202928000:  "9A",204640000:  "9B",206352000:  "9C",208064000:  "9D",
    209936000: "10A",211648000: "10B",213360000: "10C",215072000: "10D",
    216928000: "11A",218640000: "11B",220352000: "11C",222064000: "11D",
    223936000: "12A",225648000: "12B",227360000: "12C",229072000: "12D",
    230784000: "13A",232496000: "13B",234208000: "13C",235776000: "13D",237488000: "13E",239200000: "13F",

    # Band L
    # T-DAB
    1452960000: "LA",1454672000: "LB",1456384000: "LC",1458096000: "LD",
    1459808000: "LE",1461520000: "LF",1463232000: "LG",1464944000: "LH",
    1466656000: "LI",1468368000: "LJ",1470080000: "LK",1471792000: "LL",
    1473504000: "LM",1475216000: "LN",1476928000: "LO",1478640000: "LP",

    # S-DAB
    1480352000: "LQ",1482064000: "LR",1483776000: "LS",1485488000: "LT",
    1487200000: "LU",1488912000: "LV",1490624000: "LW",
}


def getRootDir():
    """Returns the absolute path to the root of the project."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def getMIBSource():
    """Returns the location of the directory where my custom MIB is located."""
    return os.path.dirname(os.path.abspath(__file__))


def __readJSON(filePath):
    with open(os.path.join(getRootDir(), filePath), "r") as f:
        return json.load(f)
def __writeJSON(filePath, data):
    with open(os.path.join(getRootDir(), filePath), "w") as f:
        json.dump(data, f)
    return data
def __updateJSON(filePath, data):
    newData = __readJSON(filePath)
    newData.update(data)
    __writeJSON(filePath, newData)
    return newData


# config.json
def getConfig():
    """Returns json object of configuration file \"config.json\"."""
    return __readJSON("config.json")
def postConfig(config):
    """Replaces configuration file \"config.json\" with json object passed in config parameter."""
    return __writeJSON("config.json", config)
def updateConfig(config):
    """Updates configuration file \"config.json\"."""
    return __updateJSON("config.json", config)


# alarmConfig.json
def getAlarmConfig():
    return __readJSON("alarmConfig.json")
def postAlarmConfig(config):
    return __writeJSON("alarmConfig.json", config)
def updateAlarmConfig(config):
    return __updateJSON("alarmConfig.json", config)


def start():
    """It is assumed that the configuration has already been set."""
    # Load the configuration
    config = getConfig()
    root = getRootDir()

    # Start SNMP_SERVER.py
    #cmd = f"nohup python3 -u {root}/SNMP_SERVER.py 1>/var/log/dabing/SNMP_SERVER.log 2>&1 &"
    #subprocess.run(cmd, shell=True)

    # Start welle-cli
    #cmd = f"nohup welle-cli -c {config['channel']} -PC 1 -w 1536 -I {config['interval']} 1>/var/log/dabing/WELLE.log 2>&1 &"
    #cmd = f"nohup welle-cli -c {config['channel']} -PC 1 -w 1536 -I {config['interval']} -f ~/recordings/dab1.raw 1>/var/log/dabing/WELLE.log 2>&1 &"
    #subprocess.run(cmd, shell=True)

    # Start EVALUATION.py
    #cmd = f"nohup python3 -u {root}/EVALUATION.py 1>/var/log/dabing/EVALUATION.log 2>&1 &"
    #subprocess.run(cmd, shell=True)
def stop():
    # Interrupt processes
    subprocess.run("pkill -SIGINT -f SNMP_SERVER.py", shell=True)
    subprocess.run("pkill -SIGINT -f welle-cli", shell=True)
    subprocess.run("pkill -SIGINT -f EVALUATION.py", shell=True)

    # Just in case
    # Kill processes if exist
    subprocess.run("pkill -SIGTERM -f SNMP_SERVER.py", shell=True)
    subprocess.run("pkill -SIGTERM -f welle-cli", shell=True)
    subprocess.run("pkill -SIGTERM -f EVALUATION.py", shell=True)


# def processConfig():
#     try:
#         with open("config.json", "r") as f:
#             response = server.make_response(f.read())
#         response.headers["Content-Type"] = "application/json"
#         return response
#     except OSError as e:
#         return (str(e), 500)

if __name__ == "__main__":

    print("Testing start() function:")
    start()