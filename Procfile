release: python manage.py migrate
web: gunicorn news_api.wsgi --log-file - --log-level debug
