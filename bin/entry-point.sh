#!/bin/sh

usermod -u $APPUID -o -m app
groupmod -g $APP_GID app

if [ $# -ge 1 ] ; then
    mode=$1
else
    mode="web"
fi

env >> /app/.env

case $mode in
    web)
        python ./manage.py runserver 0.0.0.0:8000
        ;;
    cron)
        python ./manage.py crontab add
        sudo crond -f -L /dev/stderr
        ;;
esac
