case $1 in
    gunicorn-start)
	gunicorn src.main:app -b localhost:81
	;;
    nginx-start)
	cwd=`pwd`
	nginx -c "$cwd/src/resource/nginx.conf"
	;;
    nginx-stop)
	nginx -s stop
	;;
    *)
	;;
esac
