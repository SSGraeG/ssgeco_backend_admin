#!/bin/bash

cd   /home/ubuntu/ssgAdminBE

echo ">>> pip install ----------------------"
pip install -r requirements.txt

echo ">>> remove template files ------------"
rm -rf appspec.yml requirements.txt


echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/ssgAdminBE


cd   /home/ubuntu/ssgAdminBE

touch /home/ubuntu/ssgAdminBE/log.txt

sudo chown -R ubuntu:ubuntu /home/ubuntu/ssgAdminBE/

echo ">>> start server ---------------------"
nohup flask run --host=0.0.0.0 > log.txt 2>&1 &
