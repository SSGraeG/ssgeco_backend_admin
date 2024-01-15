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
touch /home/ubuntu/flasktest.log
sudo chown ubuntu:ubuntu /home/ubuntu/flasktest.log

echo ">>> start server ---------------------"
# Flask 내장 서버로 실행 (실제 운영에서는 Gunicorn 권장)
flask run --host=0.0.0.0 --port=5000 > /dev/null 2> /home/ubuntu/flasktest.log </dev/null &
