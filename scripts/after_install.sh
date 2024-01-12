#!/bin/bash

# after_install.sh

# 원격 서버에서 실행할 명령들
ssh -i "adminBE.pem" ubuntu@10.0.132.46 << 'ENDSSH'
  # before_install.sh의 내용
  # ...

  echo ">>> pip install ----------------------"
  pip install -r requirements.txt
  pip install multidict
  echo ">>> change owner to ubuntu -----------"
  chown -R ubuntu /home/ubuntu/ssgAdminBE

  touch /home/ubuntu/ssgAdminBE/log.txt

  sudo chown -R ubuntu:ubuntu /home/ubuntu/ssgAdminBE/

  echo ">>> start server ---------------------"
  gunicorn --bind 0.0.0.0:5000 --timeout 90 app:app > /dev/null 2> /home/ubuntu/gunicorn.log </dev/null &
ENDSSH
