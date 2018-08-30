case $1 in
    start)
	gunicorn src.main:app -b localhost:81
	;;
    stop)
	;;
    *)
	;;
esac
