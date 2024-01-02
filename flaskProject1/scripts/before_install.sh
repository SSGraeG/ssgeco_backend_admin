#!/bin/bash

var=$(ps -ef | grep 'flask run --host=0.0.0.0' | grep -v 'grep')
pid=$(echo ${var} | cut -d " " -f2)
if [ -n "${pid}" ]
then
    sudo kill -9 ${pid}
    echo ${pid} is terminated.
else
    echo ${pid} is not running.
fi

rm -rf /home/ubuntu/admin_BE
mkdir  /home/ubuntu/admin_BE