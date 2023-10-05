#!/usr/bin/env bash

# setup web static
sudo apt-get -y update
sudo apt-get -y install nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

echo "<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
config='\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;}'
sed -i "38i $config" /etc/nginx/sites-available/default
service nginx restart
exit 0

