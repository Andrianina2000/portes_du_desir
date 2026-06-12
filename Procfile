web: python manage.py collectstatic --noinput && python manage.py migrate --noinput && gunicorn portes_du_desir.wsgi --workers 2 --threads 4 --timeout 120 --log-file -
