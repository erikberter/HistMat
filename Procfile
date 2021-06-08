web: gunicorn config.wsgi --log-file=-

release:python manage.py makemigrations
release:python manage.py migrate
release:python manage.py makemigrations UserMechanics
release:python manage.py migrate