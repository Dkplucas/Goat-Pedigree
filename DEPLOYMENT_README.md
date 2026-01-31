# Deployment Documentation

This directory contains comprehensive deployment documentation and scripts for the Goat Pedigree application.

## 📋 Files Overview

### Documentation Files

1. **[SERVER_CONNECTION.md](./SERVER_CONNECTION.md)** - Server access and quick deployment workflow
   - SSH connection instructions
   - Step-by-step deployment guide
   - Troubleshooting common issues
   - Rollback procedures
   - Security notes

2. **[DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)** - Detailed deployment checklist
   - Pre-deployment verification steps
   - Server configuration checks
   - Deployment procedures
   - Post-deployment verification
   - Security validation

### Script Files

3. **[verify_deployment.sh](./verify_deployment.sh)** - Automated deployment verification script
   - System health checks
   - Configuration validation
   - Service status verification
   - Run before and after deployment

4. **[quick_deploy.sh](./quick_deploy.sh)** - Quick deployment automation script
   - Automated deployment steps
   - Database backup
   - Code updates
   - Service restart

## 🚀 Quick Start

### For First-Time Deployment Setup

1. Ensure you have the SSH key file in your local machine:
   ```bash
   chmod 600 ~/.ssh/ssh-key-2025-07-13.key
   ```

2. Connect to the server:
   ```bash
   ssh -i ~/.ssh/ssh-key-2025-07-13.key ubuntu@130.61.224.177
   ```

3. Navigate to the application directory:
   ```bash
   cd /home/goat_app/apps/Goat-Pedigree
   ```

4. Run the verification script:
   ```bash
   ./verify_deployment.sh
   ```

### For Regular Deployments

Use the quick deployment script:

```bash
ssh -i ~/.ssh/ssh-key-2025-07-13.key ubuntu@130.61.224.177
cd /home/goat_app/apps/Goat-Pedigree
./quick_deploy.sh
```

Or follow the manual steps in [SERVER_CONNECTION.md](./SERVER_CONNECTION.md).

## 📖 Recommended Reading Order

1. Start with **SERVER_CONNECTION.md** for understanding server access and basic workflow
2. Review **DEPLOYMENT_CHECKLIST.md** for comprehensive deployment procedures
3. Familiarize yourself with the verification and deployment scripts

## 🔐 Security Reminders

- **NEVER** commit SSH keys to the repository
- Always verify `DEBUG = False` in production settings
- Keep database backups before major deployments
- Monitor logs after deployment
- Use environment variables for sensitive configuration

## 🆘 Need Help?

### Common Issues

**Connection refused:**
```bash
# Check if services are running
sudo systemctl status gunicorn nginx postgresql
```

**Static files not loading:**
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

**Database errors:**
```bash
python manage.py migrate
sudo systemctl restart gunicorn
```

### Where to Look

- Application logs: `sudo journalctl -u gunicorn -n 100`
- Nginx logs: `sudo tail -f /var/log/nginx/error.log`
- Django errors: Check the application output

## 📝 Before Each Deployment

- [ ] Test changes locally
- [ ] Review code changes
- [ ] Check for security vulnerabilities
- [ ] Update requirements.txt if needed
- [ ] Create database migrations if needed
- [ ] Review [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)

## 🔄 Deployment Workflow Summary

```
Local Machine                    Production Server
     │                                  │
     ├─► 1. Test & Commit              │
     │                                  │
     ├─► 2. Push to GitHub             │
     │                                  │
     ├─► 3. SSH to Server ─────────────►│
     │                                  │
     │                            4. Run verify_deployment.sh
     │                                  │
     │                            5. Backup database
     │                                  │
     │                            6. Pull changes
     │                                  │
     │                            7. Update dependencies
     │                                  │
     │                            8. Run migrations
     │                                  │
     │                            9. Collect static files
     │                                  │
     │                            10. Restart services
     │                                  │
     │                            11. Verify deployment
     │                                  │
     │                            12. Monitor logs
```

## 📊 Server Information

- **IP Address:** 130.61.224.177
- **Domains:** 
  - goatpedigree.pro
  - www.goatpedigree.pro
- **Application Path:** /home/goat_app/apps/Goat-Pedigree
- **Database:** PostgreSQL (goatpedigreedb)
- **Web Server:** Nginx
- **Application Server:** Gunicorn
- **Python:** Python 3.x with Django 4.2

## 🔧 Configuration Files

Key configuration files on the server:
- Django settings: `goat_project/settings.py`
- Gunicorn service: `/etc/systemd/system/gunicorn.service`
- Nginx config: `/etc/nginx/sites-available/goatpedigree`

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Last Updated:** 2025-01-31
**Version:** 1.0
