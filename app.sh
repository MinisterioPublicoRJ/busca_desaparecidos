gunicorn busca_desaparecidos.wsgi:application --bind=0.0.0.0:8080 --timeout 60 --log-file -
