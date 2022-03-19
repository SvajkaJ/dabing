#!/bin/bash
# Autor: SvajkaJ
# Date:  19.3.2022

# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04

# Configuring Nginx to Proxy Requests

sudo touch /etc/nginx/sites-available/dabing
sudo echo "server {
    listen 80;
    server_name localhost;

    root /home/pi/dabing;

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
