#!/bin/sh

GEN3_UWSGI_TIMEOUT="${GEN3_UWSGI_TIMEOUT:-45s}"

# fill in timeout in the uwsgi.conf template
if [ -f /etc/nginx/sites-available/uwsgi.conf ]; then
  sed -i -e "s/GEN3_UWSGI_TIMEOUT/$GEN3_UWSGI_TIMEOUT/g" /etc/nginx/sites-available/uwsgi.conf
fi

# add nginx status config
nginx_status_conf="\ \ \ \ location /nginx_status {\n\ \ \ \ \ \ stub_status;\n\ \ \ \ \ \ #allow 127.0.0.1;\n\ \ \ \ \ \ #deny all;\n\ \ \ \ \ \ access_log off;\n\ \ \ \ }"
sed -i "/\ \ \ \ error_page\ 502/i ${nginx_status_conf}" /etc/nginx/conf.d/uwsgi.conf

# add uwsgi status config
uwsgi_status_conf="\ \ \ \ location /uwsgi_status {\n\ \ \ \ \ \ proxy_pass \"http://127.0.0.1:9191\";\n\ \ \ \ \ \ #allow 127.0.0.1;\n\ \ \ \ \ \ #deny all;\n\ \ \ \ \ \ access_log off;\n\ \ \ \ }"
sed -i "/\ \ \ \ error_page\ 502/i ${uwsgi_status_conf}" /etc/nginx/conf.d/uwsgi.conf

# add another access log in a non-json format
additional_access_log_conf="\ \ \ \ access_log  /var/log/nginx/access_not_json.log main;"
sed -i "/\ \ \ \ access_log/a ${additional_access_log_conf}" /etc/nginx/nginx.conf

uwsgi --ini uwsgi.ini -H /env/ &
nginx -g 'daemon off;'
wait
