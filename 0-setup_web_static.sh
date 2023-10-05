#!/usr/bin/env bash

# update and install Nginx if not installed already
sudo apt-get -y update
sudo apt-get -y install nginx

# necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# create a HTML file
echo -e '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>' | sudo tee /data/web_static/releases/test/index.html > /dev/null

# create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# configure Nginx to serve the content
config_file="/etc/nginx/sites-available/default"
config_content="server {
    listen 80 default_server;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
    }

    location / {
        try_files \$uri \$uri/ =404;
    }
}"

echo "$config_content" | sudo tee "$config_file" > /dev/null

sudo service nginx restart

exit 0

