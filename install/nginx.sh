# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04

# Creating a systemd Unit File
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

sudo systemctl start dabing
sudo systemctl enable dabing
#sudo systemctl status dabing

# uWSGI application server should now be up and running,

# Configuring Nginx to Proxy Requests

sudo touch /etc/nginx/sites-available/dabing
sudo echo "server {
    listen 80;
    server_name localhost;

    root /home/pi/dabing;

    location / {

    }

    location /flask {
        include uwsgi_params;
        uwsgi_pass unix:/home/pi/dabing/dabing.sock;
    }

    location /welle/ {
        proxy_pass http://localhost:1536/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}" > /etc/nginx/sites-available/dabing

# To enable the Nginx server block configuration you’ve just created,
# link the file to the sites-enabled directory:
sudo ln -s /etc/nginx/sites-available/dabing /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default

# With the file in that directory,
# you can test for syntax errors by running the following:
# sudo nginx -t

sudo systemctl restart nginx

# If you encounter any errors, try checking the following:
# sudo less /var/log/nginx/error.log           checks the Nginx error logs.
# sudo less /var/log/nginx/access.log          checks the Nginx access logs.
# sudo journalctl -u nginx                     checks the Nginx process logs.
# sudo journalctl -u dabing                    checks your Flask app's uWSGI logs.

# Finishing up
sudo mkdir -p /var/log/dabing
sudo touch /var/log/dabing/SNMP_SERVER.log
sudo touch /var/log/dabing/WELLE.log
sudo touch /var/log/dabing/EVALUATION.log
sudo touch /var/log/dabing/readme.txt
#sudo chown -R pi:pi /var/log/dabing/*.log

sudo echo "If you encounter any errors,
try checking the following:
  sudo less /var/log/nginx/error.log           checks the Nginx error logs.
  sudo less /var/log/nginx/access.log          checks the Nginx access logs.
  sudo journalctl -u nginx                     checks the Nginx process logs.
  sudo journalctl -u dabing                    checks your Flask app's uWSGI logs.
" > /var/log/dabing/readme.txt
