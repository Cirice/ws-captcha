case $1 in
    start)
	  redis-server $2
	  ;;
    stop)
	#kill -p `$(cat /var/run/redis.pid)`
	;;
    *)
	echo "./db.sh start redis configuration file path; e.g: ./db.sh start /etc/redis/redis.conf"
	echo "./db.sh stop"

esac

	  
