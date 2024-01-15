#!/bin/bash

# 이전에 실행된 gunicorn 프로세스를 중지합니다.
pkill -f 'flask run --host=0.0.0.0'

# 로그 파일과 프로젝트 디렉터리를 초기화합니다.
rm -rf /home/ubuntu/flasktest.log

rm -rf /home/ubuntu/ssgAdminBE
mkdir /home/ubuntu/ssgAdminBE

cd /home/ubuntu/ssgAdminBE
