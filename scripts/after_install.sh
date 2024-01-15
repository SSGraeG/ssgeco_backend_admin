#!/bin/bash

cd /home/ubuntu/ssgAdminBE

echo ">>> pip install ----------------------"
pip install -r requirements.txt
pip install multidict
echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/ssgAdminBE


cd /home/ubuntu/ssgAdminBE

touch /home/ubuntu/ssgAdminBE/log.txt

sudo chown -R ubuntu:ubuntu /home/ubuntu/ssgAdminBE/
touch /home/ubuntu/gunicorn.log && chmod +w /home/ubuntu/gunicorn.log

echo ">>> start server ---------------------"
gunicorn --bind 0.0.0.0:5000 --timeout 90 app:app > /dev/null 2> /home/ubuntu/gunicorn.log </dev/null &