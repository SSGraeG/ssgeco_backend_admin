#!/bin/bash

# 이전에 실행된 gunicorn 프로세스를 중지합니다.
pkill -f 'gunicorn --bind 0.0.0.0:5000 --timeout 90 app:app'

# 로그 파일과 프로젝트 디렉터리를 초기화합니다.
rm -rf /home/ubuntu/gunicorn.log
rm -rf /home/ubuntu/ssgAdminBE
mkdir /home/ubuntu/ssgAdminBE

cd /home/ubuntu/ssgAdminBE
