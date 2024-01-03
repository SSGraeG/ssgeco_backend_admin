#!/bin/bash



cd /home/ubuntu/ssgAdminBE

touch /home/ubuntu/ssgAdminBE/log.txt

sudo chown -R ubuntu:ubuntu /home/ubuntu/ssgAdminBE/

echo ">>> start server ---------------------"
gunicorn --bind 0.0.0.0:5000 --timeout 90 "app:create_app()" > /dev/null 2> /home/ubuntu/gunicorn.log </dev/null &
