#!/bin/bash

cd /home/ubuntu/ssgAdminBE

echo ">>> pip install ----------------------"
pip install -r requirements.txt
pip install multidict
echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/ssgAdminBE

pip install sshtunnel
pip install multidict

cd /home/ubuntu/ssgAdminBE


touch /home/ubuntu/ssgAdminBE/log.txt

# 로그 파일의 소유자 변경
touch /home/ubuntu/gunicorn.log
sudo chown ubuntu:ubuntu /home/ubuntu/gunicorn.log


echo ">>> start server ---------------------"
# 권한 설정을 추가하고, 로그 파일을 기록 가능하도록 수정
gunicorn --bind 0.0.0.0:5000 --timeout 90 app:app > /dev/null 2> /home/ubuntu/gunicorn.log </dev/null &
