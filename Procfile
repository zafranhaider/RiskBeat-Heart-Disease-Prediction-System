Procfile

web: gunicorn health.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn health.wsgi
