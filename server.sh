case $1 in
    start)
	gunicorn src.main:app -b 0.0.0.0:80
	;;
    stop)
	;;
    *)
	;;
esac
