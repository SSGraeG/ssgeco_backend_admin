#!/bin/bash

cd /home/ubuntu/ssgAdminBE

echo ">>> pip install ----------------------"
pip install -r requirements.txt
pip install multidict
echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/ssgAdminBE

pip install sshtunnel

cd /home/ubuntu/ssgAdminBE

touch /home/ubuntu/ssgAdminBE/log.txt

# 로그 파일의 소유자 변경
sudo chown ubuntu:ubuntu /home/ubuntu/gunicorn.log
touch /home/ubuntu/gunicorn.log

echo ">>> start server ---------------------"
# 권한 설정을 추가하고, 로그 파일을 기록 가능하도록 수정
gunicorn --bind 0.0.0.0:5000 --timeout 90 app:app > /home/ubuntu/gunicorn.log 2>&1 &

# 서버가 정상적으로 실행되었는지 확인하기 위해 로그를 출력
tail -f /home/ubuntu/gunicorn.log
