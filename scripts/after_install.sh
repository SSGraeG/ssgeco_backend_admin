#!/bin/bash

cd /home/ubuntu/ssgAdminBE

echo ">>> pip install ----------------------"
pip install -r requirements.txt

echo ">>> remove template files ------------"
rm -rf appspec.yml requirements.txt

echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/ssgAdminBE

echo ">>> start server ---------------------"
gunicorn --bind 0.0.0.0:5000 app:app --workers 1 --timeout 90 > /dev/null 2> /home/ubuntu/gunicorn.log </dev/null &
