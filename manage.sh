#!/bin/bash

export CAPTCHA_DEBUG=1

app_name="src.main:app"
cwd=`pwd`

case $1 in
    gunicorn-start)
	host_port="localhost:87"
	num_workerz=10
	gunicorn $app_name -b $host_port --chdir $cwd --workers $num_workerz --daemon
	;;
    gunicorn-stop)
	kill -9 `ps aux | grep gunicorm | grep $app_name | awk '{ print $2 }' `
	;;
    nginx-start)
	nginx -c "$cwd/src/resources/nginx.conf"
	;;
    nginx-stop)
	nginx -s stop
	;;
    redis-start)
	redis-server "$cwd/src/resources/redis.conf"
	;;
    redis-stop)
	redis-cli shutdown
	;;
    start-all)
	$shell $cwd/manage.sh redis-start;
	$shell $cwd/manage.sh gunicorn-start;
	$shell $cwd/manage.sh nginx-start
	;;
    install-sys-deps)
	sudo ap-get install nginx redis-server python3-pip && \
	sudo systemctl stop nginx redis-server && \
	sudo systemctl disable nginx redis-server
	;;
    *)
	;;
esac
