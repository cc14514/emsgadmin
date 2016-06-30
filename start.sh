#!/usr/bin/env bash
ps -ef |grep emsgadmin|awk '{print $2}'|xargs kill -9
ps -ef |grep get_total_count|awk '{print $2}'|xargs kill -9
python manage.py collectstatic
rm -rf */*.pyc
rm -rf */*/*.pyc
uwsgi --http :8800 --socket :8880 --chdir `pwd` --module emsgadmin.wsgi &
cd tools/session_counter
python get_total_count.py &
