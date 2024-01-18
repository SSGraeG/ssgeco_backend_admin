#!/bin/bash
LOGFILE=/home/ubuntu/gunicorn.log

cd /home/ubuntu/ssgAdminBE

echo ">>> pip install ----------------------"
pip install -r requirements.txt

echo ">>> remove template files "
rm -rf appspec.yml requirements.txt

echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/ssgAdminBE

sudo chown ubuntu:ubuntu /home/ubuntu/ssgAdminBE

echo ">>> start server ---------------------"
gunicorn --bind 0.0.0.0:5000 --timeout 90 app:app >> "$LOGFILE" 2>&1 &