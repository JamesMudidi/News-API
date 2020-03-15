release: python manage.py migrate
web: gunicorn jeffrey.wsgi --log-file - --log-level debug
