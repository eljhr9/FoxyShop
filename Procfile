web: gunicorn django_shop.wsgi --log-file -
celery: celery worker -A django_shop -l info -c 4
