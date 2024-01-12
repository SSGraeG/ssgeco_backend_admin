#!/bin/bash

# 베스천 호스트에서 프라이빗 서브넷의 EC2로 코드를 복사하고 스크립트 실행
# 프라이빗 서브넷의 EC2에서 스크립트 실행
cd /home/ubuntu/ssgAdminBE

echo ">>> pip install ----------------------"
pip install -r requirements.txt
pip install multidict
echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/ssgAdminBE

touch /home/ubuntu/ssgAdminBE/log.txt

sudo chown -R ubuntu:ubuntu /home/ubuntu/ssgAdminBE/

echo ">>> start server ---------------------"
nohup gunicorn --bind 0.0.0.0:5000 --timeout 90 app:app > /dev/null 2> /home/ubuntu/gunicorn.log </dev/null &
