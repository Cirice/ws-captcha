#!/usr/bin/env sh


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
	nginx -c "$cwd/src/resource/nginx.conf"
	;;
    nginx-stop)
	nginx -s stop
	;;
    redis-start)
	redis-server "$cwd/src/resource/redis.conf"
	;;
    redis-stop)
	redis-cli shutdown
	;;
    *)
	;;
esac
