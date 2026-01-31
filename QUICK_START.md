# 🚀 Safe Deployment Guide - Quick Reference

## ⚡ Quick Start (For Experienced Users)

```bash
# 1. Connect to server
ssh -i ~/.ssh/ssh-key-2025-07-13.key ubuntu@130.61.224.177

# 2. Navigate and deploy
cd /home/goat_app/apps/Goat-Pedigree
./quick_deploy.sh

# 3. Verify
./verify_deployment.sh
```

## 📚 Complete Documentation Structure

```
Goat-Pedigree/
│
├── DEPLOYMENT_README.md        ← START HERE (Overview & Navigation)
│   └── Explains all deployment files and workflow
│
├── SERVER_CONNECTION.md        ← Server Access & Quick Workflow
│   ├── SSH connection instructions
│   ├── Step-by-step deployment guide
│   ├── Troubleshooting section
│   └── Rollback procedures
│
├── DEPLOYMENT_CHECKLIST.md     ← Comprehensive Checklist
│   ├── Pre-deployment checks
│   ├── Server configuration verification
│   ├── Deployment steps
│   ├── Post-deployment verification
│   └── Security validation
│
├── verify_deployment.sh        ← Automated Verification Script
│   └── Run before/after deployment to check system health
│
└── quick_deploy.sh             ← Automated Deployment Script
    └── Automates the deployment process with safety checks
```

## 🎯 Usage Scenarios

### Scenario 1: First Time Deployment
1. Read [DEPLOYMENT_README.md](./DEPLOYMENT_README.md) completely
2. Follow [SERVER_CONNECTION.md](./SERVER_CONNECTION.md) step-by-step
3. Use [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) as a guide

### Scenario 2: Regular Updates
```bash
ssh -i ~/.ssh/ssh-key-2025-07-13.key ubuntu@130.61.224.177
cd /home/goat_app/apps/Goat-Pedigree
./quick_deploy.sh
./verify_deployment.sh
```

### Scenario 3: Checking Server Health
```bash
ssh -i ~/.ssh/ssh-key-2025-07-13.key ubuntu@130.61.224.177
cd /home/goat_app/apps/Goat-Pedigree
./verify_deployment.sh
```

### Scenario 4: Emergency Rollback
See "Rollback Procedure" in [SERVER_CONNECTION.md](./SERVER_CONNECTION.md)

## 🔍 What Each File Does

| File | Purpose | When to Use |
|------|---------|-------------|
| **DEPLOYMENT_README.md** | Navigation hub & overview | Start here for any deployment task |
| **SERVER_CONNECTION.md** | Practical guide with commands | Step-by-step deployments |
| **DEPLOYMENT_CHECKLIST.md** | Detailed verification checklist | Comprehensive review & planning |
| **verify_deployment.sh** | Automated health checks | Before/after deployment |
| **quick_deploy.sh** | Automated deployment | Quick, routine deployments |

## ✅ Pre-Deployment Quick Checklist

Before connecting to the server:

- [ ] Code changes are tested locally
- [ ] All tests pass
- [ ] Changes are committed and pushed to GitHub
- [ ] You have the SSH key with correct permissions (600)
- [ ] You've reviewed what will be deployed
- [ ] You have time to monitor post-deployment (15-30 min)

## 🔐 Security Checklist

Critical security points to verify:

```bash
# On the server, check these settings:
cd /home/goat_app/apps/Goat-Pedigree

# 1. DEBUG mode must be False
grep "DEBUG = False" goat_project/settings.py

# 2. SECRET_KEY must be set
grep "SECRET_KEY" goat_project/settings.py

# 3. ALLOWED_HOSTS includes your domain
grep "ALLOWED_HOSTS" goat_project/settings.py

# 4. Check file permissions
ls -la media/
ls -la staticfiles/
```

## 🛠️ Common Commands

```bash
# View logs
sudo journalctl -u gunicorn -n 100          # Last 100 lines
sudo journalctl -u gunicorn -f              # Follow logs
sudo tail -f /var/log/nginx/error.log       # Nginx errors

# Service management
sudo systemctl status gunicorn              # Check status
sudo systemctl restart gunicorn             # Restart
sudo systemctl restart nginx                # Restart Nginx

# Django commands
python manage.py check                      # System check
python manage.py migrate --plan             # Preview migrations
python manage.py collectstatic --noinput    # Collect static files

# Database
sudo -u postgres psql -d goatpedigreedb     # Connect to DB
sudo -u postgres pg_dump goatpedigreedb > backup.sql  # Backup
```

## 📞 When Things Go Wrong

### Application won't start
```bash
sudo systemctl status gunicorn
sudo journalctl -u gunicorn -n 50 --no-pager
python manage.py check
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Database issues
```bash
python manage.py migrate
sudo systemctl status postgresql
```

### Need to rollback
```bash
git log --oneline -10  # Find previous commit
git reset --hard <commit-hash>
sudo systemctl restart gunicorn
```

## 📊 Deployment Metrics to Monitor

After deployment, monitor these for 10-15 minutes:

1. **Response Times** - Application responsiveness
2. **Error Logs** - Any new errors appearing
3. **Memory Usage** - System resource utilization
4. **Database Connections** - Connection pool status
5. **HTTP Status Codes** - Check for 500 errors

```bash
# Monitor in real-time
sudo journalctl -u gunicorn -f | grep -i error
```

## 🌐 Server Details

| Item | Value |
|------|-------|
| **IP** | 130.61.224.177 |
| **Domain** | goatpedigree.pro |
| **SSH User** | ubuntu |
| **SSH Key** | ~/.ssh/ssh-key-2025-07-13.key |
| **App Path** | /home/goat_app/apps/Goat-Pedigree |
| **Database** | PostgreSQL (goatpedigreedb) |
| **Web Server** | Nginx |
| **App Server** | Gunicorn |
| **Framework** | Django 4.2 |

## 💡 Best Practices

1. **Always backup database** before major changes
2. **Test locally first** before deploying
3. **Deploy during low traffic** periods
4. **Monitor logs** after deployment
5. **Keep rollback plan ready** with previous commit hash
6. **Document issues** encountered for future reference
7. **Never commit SSH keys** to repository
8. **Use environment variables** for sensitive data

## 📖 Documentation Hierarchy

```
Level 1: QUICK_START.md (This file)
    ↓
Level 2: DEPLOYMENT_README.md (Overview)
    ↓
Level 3: SERVER_CONNECTION.md (Practical Guide)
    ↓
Level 4: DEPLOYMENT_CHECKLIST.md (Detailed Steps)
    ↓
Level 5: Scripts (verify_deployment.sh, quick_deploy.sh)
```

## 🎓 Learning Path

1. **Beginner**: Start with this file, then read DEPLOYMENT_README.md
2. **Intermediate**: Follow SERVER_CONNECTION.md step-by-step
3. **Advanced**: Use quick_deploy.sh with DEPLOYMENT_CHECKLIST.md for reference
4. **Expert**: Customize scripts for your specific needs

---

**Need Help?** Start with [DEPLOYMENT_README.md](./DEPLOYMENT_README.md)

**Quick Deploy?** Use [quick_deploy.sh](./quick_deploy.sh)

**Step-by-Step?** Follow [SERVER_CONNECTION.md](./SERVER_CONNECTION.md)

**Complete Checklist?** See [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)

---

**Version:** 1.0  
**Last Updated:** 2025-01-31  
**Status:** ✅ Ready for Production Use
