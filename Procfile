web: gunicorn ProjEmb.wsgi:application --log-file -
worker: celery -A ProjEmb worker -l info
