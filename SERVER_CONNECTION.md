# Server Connection and Deployment Guide

## Server Access

### SSH Connection
To connect to the production server:

```bash
ssh -i ~/.ssh/ssh-key-2025-07-13.key ubuntu@130.61.224.177
```

**Important:** Ensure you have the SSH key file `ssh-key-2025-07-13.key` in your `~/.ssh/` directory with proper permissions:
```bash
chmod 600 ~/.ssh/ssh-key-2025-07-13.key
```

### Server Information
- **IP Address:** 130.61.224.177
- **Domain:** goatpedigree.pro, www.goatpedigree.pro
- **User:** ubuntu
- **Application Directory:** /home/goat_app/apps/Goat-Pedigree

## Quick Deployment Workflow

### 1. Pre-Deployment (Local)
Before connecting to the server, ensure:
- All changes are committed and pushed to the repository
- Tests pass locally
- Review the [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)

### 2. Connect to Server
```bash
ssh -i ~/.ssh/ssh-key-2025-07-13.key ubuntu@130.61.224.177
```

### 3. Navigate to Application Directory
```bash
cd /home/goat_app/apps/Goat-Pedigree
```

### 4. Run Pre-Deployment Verification
```bash
./verify_deployment.sh
```

This script will check:
- System resources (disk space, memory)
- Application directory structure
- Git status and current commit
- Python environment
- Critical files existence
- Directory permissions
- Django configuration (DEBUG mode, SECRET_KEY)
- Service status (Gunicorn, Nginx, PostgreSQL)
- Network connectivity

### 5. Backup Current State
```bash
# Backup database
sudo -u postgres pg_dump goatpedigreedb > ~/backup_$(date +%Y%m%d_%H%M%S).sql

# Backup application (optional)
tar -czf ~/goat_app_backup_$(date +%Y%m%d_%H%M%S).tar.gz /home/goat_app/apps/Goat-Pedigree/
```

### 6. Pull Latest Changes
```bash
git fetch origin
git pull origin main  # or your branch name
```

### 7. Update Application
```bash
# Activate virtual environment if exists
source venv/bin/activate  # or source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

### 8. Restart Services
```bash
# Restart Gunicorn
sudo systemctl restart gunicorn

# Check status
sudo systemctl status gunicorn

# If needed, restart Nginx
sudo systemctl restart nginx
```

### 9. Post-Deployment Verification
```bash
# Run verification script again
./verify_deployment.sh

# Check application logs
sudo journalctl -u gunicorn -n 50 --no-pager

# Test the website
curl -I https://goatpedigree.pro
```

### 10. Monitor
```bash
# Monitor logs in real-time
sudo journalctl -u gunicorn -f
```

## Troubleshooting

### If the application doesn't start:
```bash
# Check Gunicorn status
sudo systemctl status gunicorn

# View recent logs
sudo journalctl -u gunicorn -n 100 --no-pager

# Check for Python errors
python manage.py check
```

### If static files aren't loading:
```bash
# Ensure static files are collected
python manage.py collectstatic --noinput

# Check Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### Database connection issues:
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test database connection
sudo -u postgres psql -d goatpedigreedb -c "SELECT 1;"
```

### Permission issues:
```bash
# Fix media directory permissions
sudo chown -R ubuntu:ubuntu /home/goat_app/apps/Goat-Pedigree/media
sudo chmod -R 755 /home/goat_app/apps/Goat-Pedigree/media

# Fix staticfiles permissions
sudo chown -R ubuntu:ubuntu /home/goat_app/apps/Goat-Pedigree/staticfiles
sudo chmod -R 755 /home/goat_app/apps/Goat-Pedigree/staticfiles
```

## Rollback Procedure

If something goes wrong:

```bash
# Stop the service
sudo systemctl stop gunicorn

# Revert to previous commit
git log --oneline -10  # Find the previous commit hash
git reset --hard <previous-commit-hash>

# Restore database if needed (replace YYYYMMDD_HHMMSS with your actual backup timestamp)
sudo -u postgres psql goatpedigreedb < ~/backup_YYYYMMDD_HHMMSS.sql

# Restart service
sudo systemctl start gunicorn
```

## Security Notes

1. **Never commit the SSH key to the repository**
2. **Keep DEBUG = False in production**
3. **Use environment variables for sensitive data**
4. **Regularly update dependencies for security patches**
5. **Monitor logs for suspicious activity**
6. **Keep backups of database before major changes**

## Common Commands Reference

```bash
# View running processes
ps aux | grep gunicorn

# Check port usage
sudo netstat -tulpn | grep :8000

# View disk space
df -h

# View memory usage
free -m

# View system logs
sudo journalctl -xe

# Restart all services
sudo systemctl restart gunicorn nginx postgresql
```

## Configuration Files Locations

- Django settings: `/home/goat_app/apps/Goat-Pedigree/goat_project/settings.py`
- Gunicorn service: `/etc/systemd/system/gunicorn.service`
- Nginx config: `/etc/nginx/sites-available/goatpedigree`
- Database: PostgreSQL on localhost:5432

## Support and Documentation

- **Deployment Checklist:** [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)
- **Verification Script:** [verify_deployment.sh](./verify_deployment.sh)
- **Django Documentation:** https://docs.djangoproject.com/

## Emergency Contacts

Keep a list of team members who can assist with deployment issues.

---

**Last Updated:** 2025-01-31
