#!/bin/bash

var=$(ps -ef | grep 'gunicorn' | grep -v 'grep')
pid1=$(echo "${var}" | awk '{print $2}')
pid2=$(echo "${var}" | awk '{print $16}')

if [ -n "${pid1}" -a -n "${pid2}" ];
then
    sudo kill -9 "${pid1}"
    sudo kill -9 "${pid2}"
    echo "${pid1}와 ${pid2}가 종료되었습니다."
else
    echo "gunicorn 프로세스가 실행되고 있지 않습니다."
fi

rm -rf /home/ubuntu/gunicorn.log
rm -rf /home/ubuntu/ssgAdminBE
mkdir /home/ubuntu/ssgAdminBE
