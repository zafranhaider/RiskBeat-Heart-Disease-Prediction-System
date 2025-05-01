Procfile

web: gunicorn health_desease.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn health_desease.wsgi
