#!/usr/bin/python3


from flask import Flask
from flask import request, jsonify
from flask_cors import CORS

import json
import dabing
import os
import subprocess


server = Flask('Dabing', static_url_path='/')
CORS(server)

@server.route("/api/info/device") # http://192.168.178.35:5000/api/info/device
def HTTPgetDeviceInfo():
    try:
        return dabing.get_device_info()
    except:
        return ("Internal Server Error", 500)

@server.route("/api/info/status") # http://192.168.178.35:5000/api/info/status
def HTTPgetStatusInfo():
    try:
        return dabing.get_status_info()
    except:
        return ("Internal Server Error", 500)

def start():
    """It is assumed that the configuration has already been set."""
    # Load the configuration
    with open("config.json", "r") as f:
        config = json.load(f)

    # Start Welle.io
    #cmd = f"nohup ~/welle-cli -c {config['dabing']['channel']} -PC 1 -w 7575 &>$HOME/welle.io.log"
    cmd = f"nohup ~/welle-cli -c {config['dabing']['channel']} -PC 1 -w 7575 -f $HOME/recordings/dab1.raw &>$HOME/welle.io.log"
    subprocess.run(cmd, shell=True)

    # Start evaluation.py
    cmd = f"nohup python3 $HOME/dabing/dabing/evaluation.py >/dev/null 2>&1 &"
    subprocess.run(cmd, shell=True)

@server.route("/api/start") # http://192.168.178.35:5000/api/start
def HTTPstart():
    try:
        stop()  # Just in case
        start()
        return ("OK", 200)
    except:
        return ("Internal Server Error", 500)

def stop():
    # Kill processes if exist
    subprocess.run("pkill -f welle-cli", shell=True)
    subprocess.run("pkill -f evaluation.py", shell=True)

@server.route("/api/stop") # http://192.168.178.35:5000/api/stop
def HTTPstop():
    try:
        stop()
        return ("OK", 200)
    except:
        return ("Internal Server Error", 500)

#@server.route("/api/config") # http://192.168.178.35:5000/api/config
#def processConfig():
#    if request.args:
#        try:
#            newConfig = ConfigSchema().load(request.args, unknown="EXCLUDE")
#            with open("config.json", "r") as f:
#                config = json.load(f)
#            config["dabingChannel"] = newConfig["dabingChannel"]
#            with open("config.json", "w") as f:
#                f.write(json.dumps(config, indent=4))
#        except ValidationError as e:
#            return (str(e), 400)
#        except OSError as e:
#            return (str(e), 500)
#
#    try:
#        with open("config.json", "r") as f:
#            response = server.make_response(f.read())
#        response.headers["Content-Type"] = "application/json"
#        return response
#    except OSError as e:
#        return (str(e), 500)

@server.route("/api/config", methods=['GET']) # http://192.168.178.35:5000/api/config
def HTTPgetConfig():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        return jsonify(config)
    except Exception as e:
        return (str(e), 500)

@server.route("/api/config", methods=['POST']) # http://192.168.178.35:5000/api/config
def HTTPpostConfig():
    try:
        config = request.get_json()
        with open("config.json", "w") as f:
            f.write(json.dumps(config, indent=4))
        return ("OK", 200)
    except Exception as e:
        return (str(e), 500)

@server.route("/api/config", methods=['PUT']) # http://192.168.178.35:5000/api/config
def HTTPputConfig():
    try:
        newConfig = request.get_json()
        with open("config.json", "r") as f:
            config = json.load(f)

        config.update(newConfig)

        with open("config.json", "w") as f:
            f.write(json.dumps(config, indent=4))
        return ("OK", 200)
    except Exception as e:
        return (str(e), 500)

@server.route("/api/snmp") # http://192.168.178.35:5000/api/snmp
def HTTPtestSNMP():
    """Sends testing SNMP trap"""

    with open(os.path.join(os.path.expanduser('~'),"dabing/config.json"), "r") as f:
        config = json.load(f)

    host = config['snmp']['managerHostname']
    port = config['snmp']['managerPort']
    payload = f"Agent \"{config['snmp']['agentIdentifier']}\" with hostname \"{config['snmp']['agentHostname']}\" is testing SNMP Trap."

    dabing.testTrap(host, port, payload)

    return ("OK", 200)

if __name__ == "__main__":
    server.run(debug=True, host="0.0.0.0", port=5000)
