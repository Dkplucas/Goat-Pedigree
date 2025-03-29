#!/bin/bash

# Rest of your build commands
pip install -r requirements.txt
python manage.py migrate
# Add to your build script
npm install tailwindcss && \
npx tailwindcss -i ./static/css/src/input.css -o ./static/css/dist/styles.css && \
python manage.py collectstatic --noinput && \
gunicorn goat_project.wsg