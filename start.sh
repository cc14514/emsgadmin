python manage.py collectstatic
rm -rf */*.pyc
rm -rf */*/*.pyc
uwsgi --http :8800 --socket :8880 --chdir `pwd` --module django_wsgi
