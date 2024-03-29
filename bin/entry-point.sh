#!/bin/sh

if [ $# -ge 1 ] ; then
    mode=$1
else
    mode="web"
fi

env >> /app/.env

case $mode in
    init)
	python ./manage.py migrate
	python ./manage.py loaddata initial
	;;
    web)
        python ./manage.py runserver 0.0.0.0:8000
        ;;
    cron)
        python ./manage.py crontab add
        crond -f -L /dev/stderr
        ;;
esac
