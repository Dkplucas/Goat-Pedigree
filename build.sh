#!/bin/bash

# Rest of your build commands
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate