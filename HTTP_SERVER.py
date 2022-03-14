#!/usr/bin/python3
# Autor: SvajkaJ
# Datum: 27.2.2022

from flask import Flask
from flask import request, jsonify
from flask_cors import CORS                 # type: ignore
from flask_expects_json import expects_json # type: ignore

import dabing

server = Flask('Dabing', static_url_path='/')
CORS(server)


@server.route("/flask/info/device") # http://192.168.178.35:5000/flask/info/device
def HTTP_GET_flask_info_device():
    try:
        return dabing.get_device_info()
    except:
        return ("Internal Server Error", 500)

@server.route("/flask/info/status") # http://192.168.178.35:5000/flask/info/status
def HTTP_GET_flask_info_status():
    try:
        # get_status_info returns list => we need jsonify
        return jsonify(dabing.get_status_info(dabing.getConfig()))
    except:
        return ("Internal Server Error", 500)

@server.route("/flask/start") # http://192.168.178.35:5000/flask/start
def HTTP_GET_flask_start():
    try:
        dabing.stop()  # Just in case
        if dabing.start():
            return ("OK", 200)
        else:
            return ("Bad Request", 400)
    except:
        return ("Internal Server Error", 500)

@server.route("/flask/stop") # http://192.168.178.35:5000/flask/stop
def HTTP_GET_flask_stop():
    try:
        dabing.stop()
        return ("", 204)
    except:
        return ("Internal Server Error", 500)


@server.route("/flask/config/general", methods=['GET'])
def HTTP_GET_flask_config_general():
    try:
        return dabing.getConfig()
    except Exception as e:
        return (str(e), 500)

@server.route("/flask/config/general", methods=['POST'])
# Sanitizing input
@expects_json(dabing.generalConfigSchema)            # type: ignore
def HTTP_POST_flask_config_general():
    try:
        config = request.get_json()
        dabing.postConfig(config)
        return ("OK", 200)
    except Exception as e:
        return (str(e), 500)


@server.route("/flask/config/alarm", methods=['GET'])
def HTTP_GET_flask_config_alarm():
    try:
        return dabing.getAlarmConfig()
    except Exception as e:
        return (str(e), 500)

@server.route("/flask/config/alarm", methods=['POST'])
# Sanitizing input
@expects_json(dabing.alarmConfigSchema)            # type: ignore
def HTTP_POST_flask_config_alarm():
    try:
        config = request.get_json()
        dabing.postAlarmConfig(config)
        return ("OK", 200)
    except Exception as e:
        return (str(e), 500)


@server.route("/flask/snmp/test")
def HTTP_GET_flask_snmp_test():
    """Tests SNMP trap."""

    config = dabing.getConfig()

    host = config['managerHostname']
    port = config['managerPort']
    payload = f"Agent \"{config['agentIdentifier']}\" with label \"{config['agentLabel']}\" is testing SNMP Trap."

    dabing.testTrap(host, port, payload)

    return ("OK", 200)

if __name__ == "__main__":
    #server.run(debug=True, host="0.0.0.0", port=5000)
    server.run()
