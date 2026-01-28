web: gunicorn ai_club.wsgi:application --log-file -
release: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py create_admin
