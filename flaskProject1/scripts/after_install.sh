#!/bin/bash

cd   /home/ubuntu/admin_BE

echo ">>> pip install ----------------------"
pip install -r requirements.txt

echo ">>> remove template files ------------"
rm -rf appspec.yml requirements.txt


echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/admin_BE


cd   /home/ubuntu/admin_BE

touch /home/ubuntu/admin_BE/log.txt

sudo chown -R ubuntu:ubuntu /home/ubuntu/admin_BE/

echo ">>> start server ---------------------"
nohup flask run --host=0.0.0.0 > log.txt 2>&1 &