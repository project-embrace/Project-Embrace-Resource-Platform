web: gunicorn ProjEmb.wsgi:application --log-file -
worker: celery -A ProjEmb beat -l info
