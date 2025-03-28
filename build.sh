#!/bin/bash
# Create media directory if it doesn't exist
mkdir -p /var/data/media

# Set correct permissions (Render uses user 'render')
chown -R render:render /var/data/media
chmod -R 755 /var/data/media

# Rest of your build commands
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate