#!/usr/bin/python3
# Autor: SvajkaJ
# Datum: 27.2.2022


import json
import os
import subprocess

try:
    from .status import get_status_info
except:
    from status import get_status_info

freq = [
    "174928","176640","178352","180064",
    "181936","183648","185360","187072",
    "188928","190640","192352","194064",
    "195936","197648","199360","201072",
    "202928","204640","206352","208064",
    "209936","211648","213360","215072",
    "216928","218640","220352","222064",
    "223936","225648","227360","229072",
    "230784","232496","234208","235776","237488","239200"
]

channel = [
     "5A", "5B", "5C", "5D",
     "6A", "6B", "6C", "6D",
     "7A", "7B", "7C", "7D",
     "8A", "8B", "8C", "8D",
     "9A", "9B", "9C", "9D",
    "10A","10B","10C","10D",
    "11A","11B","11C","11D",
    "12A","12B","12C","12D",
    "13A","13B","13C","13D","13E","13F"
]

band = [
    {
        "key": i + 1,
        "freq": f,
        "channel": c
    } for i, (f, c) in enumerate(zip(freq, channel))
]

generalConfigSchema = {
    "type": "object",
    "properties": {
        "band": {
            "type": "object",
            "enum": band
        },
        "interval": { "type": "integer", "minimum": 96 },
        "trapEnabled": { "type": "boolean" },
        "agentIdentifier": { "type": "integer", "minimum": 0 },
        "agentLabel": { "type": "string" },
        "managerHostname": {
            "type": "string",
            "pattern": "^(?!0)(?!.*\\.$)((1?\\d?\\d|25[0-5]|2[0-4]\\d)(\\.|$)){4}$"
        },
        "managerPort": { "type": "integer", "exclusiveMinimum": 0, "maximum": 65535 }
    },
    "required": ["band", "interval", "trapEnabled", "agentIdentifier", "agentLabel", "managerHostname", "managerPort"],
    "additionalProperties": False
}

alarmConfigSchema = {
    "type": "object",
    "properties": {
        "snr": { "$ref": "#/$defs/element" },
        "ber": { "$ref": "#/$defs/element" },
        "power": { "$ref": "#/$defs/element" },
        "fiber": { "$ref": "#/$defs/element" },
        "signal": { "$ref": "#/$defs/element" },
        "sync": { "$ref": "#/$defs/element" }
    },
    "required": ["snr", "ber", "power", "fiber", "signal", "sync"],
    "additionalProperties": False,
    "$defs": {
        "element": {
            "type": "object",
            "properties": {
                "enabled": { "type": "boolean" },
                "low": { "type": "number" },
                "high": { "type": "number" },
                "trigger": { "type": "number" },
            },
            "required": ["enabled", "low", "high", "trigger"]
        }
    }
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


def get_status(config):
    s = get_status_info(config)
    subS = [x for x in s if x['isOk'] == False]
    return (len(subS) == 0)


def start():
    """It is assumed that the configuration has already been set."""
    # Load the configuration
    config = getConfig()
    root = getRootDir()

    # Start SNMP_SERVER.py
    cmd = f"nohup python3 -u {root}/SNMP_SERVER.py 1>/var/log/dabing/SNMP_SERVER.log 2>&1 &"
    subprocess.run(cmd, shell=True)

    # Start welle-cli
    #cmd = f"nohup welle-cli -c {config['band']['channel']} -PC 1 -w 1536 -I {config['interval']} 1>/var/log/dabing/WELLE.log 2>&1 &"
    cmd = f"nohup welle-cli -c {config['band']['channel']} -PC 1 -w 1536 -I {config['interval']} -f ~/recordings/dab_229072kHz_fs2048kHz_gain42_1_long.raw 1>/var/log/dabing/WELLE.log 2>&1 &"
    subprocess.run(cmd, shell=True)

    if (config['trapEnabled']):
        # Start EVALUATION.py
        cmd = f"nohup python3 -u {root}/EVALUATION.py 1>/var/log/dabing/EVALUATION.log 2>&1 &"
        subprocess.run(cmd, shell=True)

    return get_status(config)

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

    #print("Testing start() function:")
    #start()
    print(generalConfigSchema)