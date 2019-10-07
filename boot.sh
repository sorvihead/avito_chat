#!/bin/sh
source venv/bin/activate
flask db upgrade
exec gunicorn -b :9000 --access-logfile - --error-logfile - chat:app