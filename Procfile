release: python manage.py migrate
web: gunicorn TravelAI_Backend.wsgi --log-file -

worker: python manage.py rqworker high default low