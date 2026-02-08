# Deployment Checklist for Goat Pedigree Application

## Pre-Deployment Verification

This checklist ensures safe deployment of new commits to the production server at `130.61.224.177`.

### Server Access
```bash
ssh -i ~/.ssh/ssh-key-2025-07-13.key ubuntu@130.61.224.177
```

## 1. Pre-Deployment Checks (Local)

- [ ] All tests pass locally
- [ ] Code has been reviewed and approved
- [ ] No sensitive data or credentials in code
- [ ] `.gitignore` is properly configured
- [ ] Requirements are up to date in `requirements.txt`
- [ ] Database migrations are created and tested
- [ ] Static files collected and tested

## 2. Server Configuration Verification

### 2.1 System Health
```bash
# Check system resources
df -h                    # Disk space
free -m                  # Memory usage
top -bn1 | head -20      # CPU and processes
```

### 2.2 Application Status
```bash
# Check if application is running
sudo systemctl status gunicorn
sudo systemctl status nginx

# Check application logs
sudo journalctl -u gunicorn -n 50 --no-pager
sudo tail -f /var/log/nginx/error.log
```

### 2.3 Database Connectivity
```bash
# Test PostgreSQL connection
sudo -u postgres psql -c "SELECT version();"
sudo -u postgres psql -d goatpedigreedb -c "SELECT COUNT(*) FROM django_migrations;"
```

### 2.4 File Permissions
```bash
# Verify directory permissions
ls -la /home/goat_app/apps/Goat-Pedigree/
ls -la /home/goat_app/apps/Goat-Pedigree/media/
ls -la /home/goat_app/apps/Goat-Pedigree/staticfiles/
```

### 2.5 Environment Variables
```bash
# Check if .env file exists and has required variables
cat /home/goat_app/apps/Goat-Pedigree/.env
```

## 3. Deployment Steps

### 3.1 Backup Current State
```bash
# Backup database
sudo -u postgres pg_dump goatpedigreedb > ~/backup_$(date +%Y%m%d_%H%M%S).sql

# Backup application directory
tar -czf ~/goat_app_backup_$(date +%Y%m%d_%H%M%S).tar.gz /home/goat_app/apps/Goat-Pedigree/
```

### 3.2 Pull Latest Changes
```bash
cd /home/goat_app/apps/Goat-Pedigree/
git fetch origin
git status
git pull origin main  # or your target branch
```

### 3.3 Update Dependencies
```bash
# Activate virtual environment (if using one)
source venv/bin/activate

# Install/update requirements
pip install -r requirements.txt
```

### 3.4 Run Migrations
```bash
python manage.py migrate --plan  # Check what will be migrated
python manage.py migrate         # Apply migrations
```

### 3.5 Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 3.6 Restart Services
```bash
# Restart gunicorn
sudo systemctl restart gunicorn
sudo systemctl status gunicorn

# Restart nginx (if needed)
sudo systemctl restart nginx
sudo systemctl status nginx
```

## 4. Post-Deployment Verification

### 4.1 Application Health Check
```bash
# Check if site is responding
curl -I http://localhost:8000
curl -I https://goatpedigree.pro
```

### 4.2 Check Logs for Errors
```bash
# Check recent logs
sudo journalctl -u gunicorn -n 100 --no-pager | grep -i error
sudo tail -n 50 /var/log/nginx/error.log
```

### 4.3 Test Critical Functionality
- [ ] Homepage loads correctly
- [ ] User authentication works
- [ ] Goat pedigree viewing works
- [ ] Admin panel is accessible
- [ ] Static files (CSS, JS, images) load properly
- [ ] Media files are accessible

### 4.4 Monitor Performance
```bash
# Monitor for 5-10 minutes after deployment
sudo journalctl -u gunicorn -f
```

## 5. Rollback Procedure (If Needed)

If issues are detected:

```bash
# Stop services
sudo systemctl stop gunicorn

# Restore from backup
cd /home/goat_app/apps/Goat-Pedigree/
git reset --hard <previous-commit-hash>

# Restore database if migrations caused issues (replace YYYYMMDD_HHMMSS with your actual backup timestamp)
sudo -u postgres psql goatpedigreedb < ~/backup_YYYYMMDD_HHMMSS.sql

# Restart services
sudo systemctl start gunicorn
sudo systemctl restart nginx
```

## 6. Security Checks

- [ ] DEBUG mode is set to False in production
- [ ] SECRET_KEY is properly set and secure
- [ ] ALLOWED_HOSTS includes correct domains
- [ ] Database credentials are secure
- [ ] CSRF protection is enabled
- [ ] SSL/HTTPS is properly configured
- [ ] File upload permissions are correct
- [ ] No sensitive data in logs

## 7. Configuration Validation

Key settings to verify in `settings.py`:
- `DEBUG = False`
- `SECRET_KEY` is set and unique
- `ALLOWED_HOSTS` includes production domains
- Database settings point to production database
- `STATIC_ROOT` and `MEDIA_ROOT` are correct
- Email settings are configured
- Security headers are enabled

## Notes

- Always perform deployments during low-traffic periods
- Keep a communication channel open during deployment
- Have the previous working commit hash ready for quick rollback
- Document any issues encountered for future reference
- Update this checklist as the deployment process evolves
