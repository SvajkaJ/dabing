#!/bin/bash
# Autor: SvajkaJ
# Date:  19.3.2022

# --------------------------------------------- #
# Creating a systemd Unit File for uWSGI flask HTTP_SERVER.py
# Creating a systemd unit file will allow init system
# to automatically start uWSGI and serve the Flask application
# whenever the server boots.
sudo touch /etc/systemd/system/dabing.service
sudo echo "[Unit]
Description=uWSGI instance to serve dabing
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=/home/pi/dabing
ExecStart=/home/pi/.local/bin/uwsgi --ini dabing.ini

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/dabing.service

sudo systemctl enable dabing
sudo systemctl start dabing
#sudo systemctl status dabing

# uWSGI application server should now be up and running,

# --------------------------------------------- #
# Creating a systemd Unit File for SNMP_SERVER.py
sudo touch /etc/systemd/system/snmp.service
sudo echo "[Unit]
Description=systemd of SNMP_SERVER.py
After=multi-user.target

[Service]
User=pi
Group=pi
Type=simple
Restart=always
ExecStart=/usr/bin/python3 -u /home/pi/dabing/SNMP_SERVER.py 

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/snmp.service

sudo systemctl enable snmp
sudo systemctl start snmp
#sudo systemctl status snmp

# If you encounter any errors, try checking the following:
# sudo less /var/log/nginx/error.log           checks the Nginx error logs.
# sudo less /var/log/nginx/access.log          checks the Nginx access logs.
# sudo journalctl -u nginx                     checks the Nginx process logs.
# sudo journalctl -u dabing                    checks your Flask app's uWSGI logs.
# sudo journalctl -u snmp                      checks SNMP_SERVER.py related logs.

# Finishing
sudo mkdir -p /var/log/dabing
sudo touch /var/log/dabing/WELLE.log
sudo touch /var/log/dabing/EVALUATION.log
#sudo chown -R pi:pi /var/log/dabing/*

sudo touch /var/log/dabing/readme.txt
sudo echo "If you encounter any errors,
try checking the following:
  sudo less /var/log/nginx/error.log           checks the Nginx error logs.
  sudo less /var/log/nginx/access.log          checks the Nginx access logs.
  sudo journalctl -u nginx                     checks the Nginx process logs.
  sudo journalctl -u dabing                    checks your Flask app's uWSGI logs.
  sudo journalctl -u snmp                      checks SNMP_SERVER.py related logs.
" > /var/log/dabing/readme.txt
