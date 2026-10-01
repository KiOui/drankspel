#!/bin/sh

echo "🔍 Checking database connection..."
uv run manage.py check --database=default

echo "📊 Checking migration status..."
uv run manage.py showmigrations --plan

echo "🚀 Running migrations..."
uv run manage.py migrate --noinput

touch -a /log/uwsgi.log
touch -a /log/django.log

chown --recursive nobody:nogroup /log/

chown --recursive nobody:nogroup /app

echo "🌐 Starting uWSGI server..."
uv run uwsgi --chdir=/app \
    --module=drankspel.wsgi:application \
    --master --pidfile=/tmp/project-master.pid \
    --socket=:8000 \
    --processes=5 \
    --uid=nobody --gid=nogroup \
    --harakiri=60 \
    --post-buffering=16384 \
    --max-requests=5000 \
    --thunder-lock \
    --vacuum \
    --logfile-chown \
    --logto2=/log/uwsgi.log \
    --ignore-sigpipe \
    --ignore-write-errors \
    --disable-write-exception \
    --enable-threads \
    --py-call-uwsgi-fork-hooks \
    --buffer-size 32768