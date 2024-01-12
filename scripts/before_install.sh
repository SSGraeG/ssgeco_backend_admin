#!/bin/bash

# before_install.sh

# SSH로 원격 서버에 접속하고 코드를 전송하는 부분
scp -i "adminBE.pem" -r /path/to/local/code ubuntu@10.0.132.46:/home/ubuntu/ssgAdminBE

# 원격 서버에서 실행할 명령들
ssh -i "adminBE.pem" ubuntu@10.0.132.46 << 'ENDSSH'
  # 이전에 실행된 gunicorn 프로세스를 중지합니다.
  pkill -f 'gunicorn --bind 0.0.0.0:5000 --timeout 90 app:app'

  # 로그 파일과 프로젝트 디렉터리를 초기화합니다.
  rm -rf /home/ubuntu/gunicorn.log
  rm -rf /home/ubuntu/ssgAdminBE
  mkdir /home/ubuntu/ssgAdminBE

  cd /home/ubuntu/ssgAdminBE
ENDSSH
