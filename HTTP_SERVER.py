#!/usr/bin/python3
# Autor: SvajkaJ
# Datum: 27.2.2022

from flask import Flask
from flask import request, jsonify
from flask_cors import CORS            # type: ignore

import dabing

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

@server.route("/api/start") # http://192.168.178.35:5000/api/start
def HTTPstart():
    try:
        dabing.stop()  # Just in case
        dabing.start()
        return ("OK", 200)
    except:
        return ("Internal Server Error", 500)

@server.route("/api/stop") # http://192.168.178.35:5000/api/stop
def HTTPstop():
    try:
        dabing.stop()
        return ("OK", 200)
    except:
        return ("Internal Server Error", 500)

@server.route("/api/config", methods=['GET']) # http://192.168.178.35:5000/api/config
def HTTPgetConfig():
    try:
        config = dabing.getConfig()
        return jsonify(config)
    except Exception as e:
        return (str(e), 500)

@server.route("/api/config", methods=['POST']) # http://192.168.178.35:5000/api/config
def HTTPpostConfig():
    try:
        config = request.get_json()
        dabing.postConfig(config)
        return ("OK", 200)
    except Exception as e:
        return (str(e), 500)

@server.route("/api/config", methods=['PUT']) # http://192.168.178.35:5000/api/config
def HTTPupdateConfig():
    try:
        config = request.get_json()
        dabing.updateConfig(config)
        return ("OK", 200)
    except Exception as e:
        return (str(e), 500)


@server.route("/api/snmp") # http://192.168.178.35:5000/api/snmp
def HTTPtestTrap():
    """Sends testing SNMP trap"""

    config = dabing.getConfig()

    host = config['managerHostname']
    port = config['managerPort']
    payload = f"Agent \"{config['agentIdentifier']}\" with hostname \"{config['agentHostname']}\" is testing SNMP Trap."

    dabing.testTrap(host, port, payload)

    return ("OK", 200)

if __name__ == "__main__":
    server.run(debug=True, host="0.0.0.0", port=5000)
