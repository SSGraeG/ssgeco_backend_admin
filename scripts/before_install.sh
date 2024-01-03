#!/bin/bash

cd /home/ubuntu/ssgAdminBE

echo ">>> pip install ----------------------"
pip install -r requirements.txt
pip install flask-cors  # Install flask-cors explicitly

echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/ssgAdminBE

var=$(ps -ef | grep 'gunicorn' | grep -v 'grep')
pid1=$(echo ${var} | cut -d " " -f2)
pid2=$(echo ${var} | cut -d " " -f16)

if [ -n "${pid1}" ] && [ -n "${pid2}" ];
then
    sudo kill -9 "${pid1}"
    sudo kill -9 "${pid2}"
    echo "${pid1} and ${pid2} are terminated."
else
    echo "gunicorn processes are not running."
fi

# Wait for existing processes to be terminated
sleep 5

rm -rf /home/ubuntu/gunicorn.log

rm -rf /home/ubuntu/ssgAdminBE
mkdir  /home/ubuntu/ssgAdminBE
