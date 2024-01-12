#!/bin/bash

# 코드를 베스천 호스트로 복사
scp -i "adminBE.pem" -r /path/to/local/code ubuntu@10.0.132.46:/home/ubuntu/ssgAdminBE

# 베스천 호스트에서 프라이빗 서브넷의 EC2로 코드를 복사하고 스크립트 실행
ssh -i "adminBE.pem" ubuntu@10.0.132.46 << 'ENDSSH'
  # 이전에 실행된 gunicorn 프로세스를 중지합니다.
  pkill -f 'gunicorn --bind 0.0.0.0:5000 --timeout 90 app:app'

  # 로그 파일과 프로젝트 디렉터리를 초기화합니다.
  rm -rf /home/ubuntu/gunicorn.log
  rm -rf /home/ubuntu/ssgAdminBE
  mkdir /home/ubuntu/ssgAdminBE

  # 코드를 프라이빗 서브넷의 EC2로 복사
  scp -r /home/ubuntu/ssgAdminBE ubuntu@private-subnet-ip:/home/ubuntu

  # 프라이빗 서브넷의 EC2에서 스크립트 실행
  ssh -i "adminBE.pem" ubuntu@private-subnet-ip << 'INNER_SSH'
    cd /home/ubuntu/ssgAdminBE
  INNER_SSH
ENDSSH
