release: python manage.py makemigrations
release: python manage.py migrate
release: python manage.py makemigrations UserMechanics
release: python manage.py migrate
release: python manage.py createcachetable
web: gunicorn config.wsgi --preload --log-file -


