#!/bin/sh

GEN3_UWSGI_TIMEOUT="${GEN3_UWSGI_TIMEOUT:-45s}"

# fill in timeout in the uwsgi.conf template
if [ -f /etc/nginx/sites-available/uwsgi.conf ]; then
  sed -i -e "s/GEN3_UWSGI_TIMEOUT/$GEN3_UWSGI_TIMEOUT/g" /etc/nginx/sites-available/uwsgi.conf
fi

sed -i "/\ \ \ \ error_page\ 502/i ${nginx_status_conf}" /etc/nginx/conf.d/uwsgi.conf

uwsgi --ini uwsgi.ini -H /env/ &
nginx -g 'daemon off;'
wait
