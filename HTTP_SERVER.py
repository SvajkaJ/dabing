#!/usr/bin/python3
# Autor: SvajkaJ
# Datum: 27.2.2022

from flask import Flask
from flask import request, jsonify
from flask_cors import CORS            # type: ignore

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
        return jsonify(dabing.get_status_info())
    except:
        return ("Internal Server Error", 500)

@server.route("/flask/start") # http://192.168.178.35:5000/flask/start
def HTTPstart():
    try:
        dabing.stop()  # Just in case
        if dabing.start():
            return ("OK", 200)
        else:
            return ("Bad Request", 400)
    except:
        return ("Internal Server Error", 500)

@server.route("/flask/stop") # http://192.168.178.35:5000/flask/stop
def HTTPstop():
    try:
        dabing.stop()
        return ("", 204)
    except:
        return ("Internal Server Error", 500)


@server.route("/flask/config/general", methods=['GET'])
def HTTP_GET_flask_config_general():
    try:
        config = dabing.getConfig()
        return jsonify(config)
    except Exception as e:
        return (str(e), 500)

@server.route("/flask/config/general", methods=['POST'])
def HTTP_POST_flask_config_general():
    try:
        config = request.get_json()
        dabing.postConfig(config)
        return ("OK", 200)
    except Exception as e:
        return (str(e), 500)

@server.route("/flask/config/general", methods=['PUT']) # http://192.168.178.35:5000/flask/config
def HTTP_PUT_flask_config_general():
    try:
        config = request.get_json()
        dabing.updateConfig(config)
        return ("OK", 200)
    except Exception as e:
        return (str(e), 500)


@server.route("/flask/config/alarm", methods=['GET'])
def HTTP_GET_flask_config_alarm():
    try:
        config = dabing.getAlarmConfig()
        return jsonify(config)
    except Exception as e:
        return (str(e), 500)

@server.route("/flask/config/alarm", methods=['POST'])
def HTTP_POST_flask_config_alarm():
    try:
        config = request.get_json()
        dabing.postAlarmConfig(config)
        return ("OK", 200)
    except Exception as e:
        return (str(e), 500)


@server.route("/flask/snmp") # http://192.168.178.35:5000/flask/snmp
def HTTPtestTrap():
    """Sends testing SNMP trap"""

    config = dabing.getConfig()

    host = config['managerHostname']
    port = config['managerPort']
    payload = f"Agent \"{config['agentIdentifier']}\" with hostname \"{config['agentHostname']}\" is testing SNMP Trap."

    dabing.testTrap(host, port, payload)

    return ("OK", 200)

if __name__ == "__main__":
    #server.run(debug=True, host="0.0.0.0", port=5000)
    server.run()
