#!/bin/bash

# Add these lines at the top
pip install --upgrade pip setuptools wheel
pip install PyYAML==6.0.1

# Exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate