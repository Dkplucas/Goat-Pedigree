#!/usr/bin/env bash
set -o errexit
mkdir -p media/goats
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput