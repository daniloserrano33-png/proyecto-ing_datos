#!/bin/bash
# Install DB driver for postgres
pip install psycopg2-binary
# Initialize Superset
superset db upgrade
superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin
superset init
# Start webserver
gunicorn --bind "0.0.0.0:8088" --access-logfile '-' --error-logfile '-' --timeout 120 --workers 1 --worker-class gthread --threads 20 "superset.app:create_app()"
