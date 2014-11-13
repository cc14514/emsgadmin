# python manage.py collectstatic
uwsgi --http :8800 --socket :8880 --chdir `pwd` --module django_wsgi
