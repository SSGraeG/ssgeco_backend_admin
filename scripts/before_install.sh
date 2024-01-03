
#!/bin/bash

var=$(ps -ef | grep 'gunicorn' | grep -v 'grep')
pid1=$(echo ${var} | cut -d " " -f2)
pid2=$(echo ${var} | cut -d " " -f16)

if [ -n "${pid1}" ] && [ -n "${pid2}" ];
then
    sudo kill -9 ${pid1}
    sudo kill -9 ${pid2}
    echo "${pid1} and ${pid2} are terminated."
else
    echo "gunicorn processes are not running."
fi

rm -rf /home/ubuntu/gunicorn.log

rm -rf /home/ubuntu/ssgAdminBE
mkdir /home/ubuntu/ssgAdminBE
