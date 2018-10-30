#!/bin/bash
set -e

# run migrations
/app/src/OIPA/manage.py migrate --noinput

# generate static files
/app/src/OIPA/manage.py collectstatic --noinput

# run Django as a wsgi process
/app/src/bin/wait-for-postgres.sh -- uwsgi \
    --chdir=/app/src/OIPA \
    --module=OIPA.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=OIPA.settings \
    --master \
    --pidfile=/tmp/uwsgi.pid \
    --thunder-lock \
    --http 0.0.0.0:8000 \
    --buffer-size 32768 \
    --processes=3 \
    --uid=1000 \
    --gid=1000 \
    --vacuum \
    --harakiri=120 \
