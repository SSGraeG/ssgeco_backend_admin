#!/bin/bash

cd /home/ubuntu/ssgAdminBE

echo ">>> pip install ----------------------"
pip install -r requirements.txt
echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/ssgAdminBE

# 기존에 실행 중인 gunicorn 프로세스를 종료합니다.
pkill gunicorn

# Wait for existing processes to be terminated
sleep 5

# 로그 파일과 프로젝트 디렉터리를 초기화합니다.
rm -rf /home/ubuntu/gunicorn.log
rm -rf /home/ubuntu/ssgAdminBE
mkdir /home/ubuntu/ssgAdminBE
