# 🐐 Goat Pedigree Application

A Django-based web application for managing and tracking goat pedigrees.

## 🌐 Production Site

- **Website:** https://goatpedigree.pro
- **Server IP:** 130.61.224.177

## 🚀 Deployment Documentation

This repository includes comprehensive deployment documentation for safely deploying updates to the production server.

### 📚 Documentation Files

| File | Description | Use Case |
|------|-------------|----------|
| **[QUICK_START.md](./QUICK_START.md)** | Quick reference guide | Fast lookup for experienced users |
| **[DEPLOYMENT_README.md](./DEPLOYMENT_README.md)** | Documentation overview | Navigation hub for all deployment docs |
| **[SERVER_CONNECTION.md](./SERVER_CONNECTION.md)** | Server access guide | SSH connection and step-by-step deployment |
| **[DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)** | Comprehensive checklist | Detailed verification and procedures |

### 🛠️ Deployment Scripts

| Script | Purpose |
|--------|---------|
| **[verify_deployment.sh](./verify_deployment.sh)** | Automated health and configuration checks |
| **[quick_deploy.sh](./quick_deploy.sh)** | Automated deployment with safety measures |

## 🎯 Quick Deployment

For routine deployments:

```bash
# 1. Connect to server
ssh -i ~/.ssh/ssh-key-2025-07-13.key ubuntu@130.61.224.177

# 2. Deploy
cd /home/goat_app/apps/Goat-Pedigree
./quick_deploy.sh

# 3. Verify
./verify_deployment.sh
```

## 📖 Getting Started with Deployment

**New to deployment?** Start here:
1. Read [QUICK_START.md](./QUICK_START.md)
2. Then follow [SERVER_CONNECTION.md](./SERVER_CONNECTION.md)

**Experienced user?**
- Use [quick_deploy.sh](./quick_deploy.sh) for automated deployment
- Reference [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) as needed

## 🏗️ Technology Stack

- **Backend:** Django 4.2
- **Database:** PostgreSQL
- **Web Server:** Nginx
- **Application Server:** Gunicorn
- **Frontend:** Tailwind CSS
- **Python:** 3.x

## 🔐 Security

- Production environment with `DEBUG = False`
- HTTPS enabled via SSL certificates
- CSRF protection enabled
- Secure cookie settings
- Database credentials stored securely

**Important:** Never commit sensitive data or SSH keys to the repository. See [.gitignore](./.gitignore) for protected files.

## 🧪 Development Setup

```bash
# Clone the repository
git clone https://github.com/Dkplucas/Goat-Pedigree.git
cd Goat-Pedigree

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create media directories
mkdir -p media/goats

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

## 📁 Project Structure

```
Goat-Pedigree/
├── goat_project/          # Django project settings
│   ├── settings.py        # Main configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI configuration
├── goats/                # Main application
├── media/                # User-uploaded files
├── static/               # Static assets
├── staticfiles/          # Collected static files
├── theme/                # Tailwind theme
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── build.sh             # Build script
└── [Deployment Docs]    # See documentation files above
```

## 🔧 Management Commands

```bash
# Database operations
python manage.py migrate              # Apply migrations
python manage.py makemigrations       # Create migrations
python manage.py createsuperuser      # Create admin user

# Static files
python manage.py collectstatic        # Collect static files

# Development
python manage.py runserver            # Run dev server
python manage.py shell               # Django shell

# Testing
python manage.py test                # Run tests
```

## 🌟 Features

- Goat pedigree management
- User authentication
- Admin interface
- Media file uploads
- RESTful API (Django REST Framework)
- Responsive design with Tailwind CSS
- CORS support
- Import/Export functionality

## 📝 Configuration

Key configuration files:
- `goat_project/settings.py` - Main Django settings
- `.env` - Environment variables (not committed)
- `requirements.txt` - Python package dependencies

## 🔄 Deployment Workflow

```
1. Local Development → 2. Testing → 3. Git Commit/Push
                                           ↓
                                    4. SSH to Server
                                           ↓
                                    5. Run Verification
                                           ↓
                                    6. Backup Database
                                           ↓
                                    7. Deploy Changes
                                           ↓
                                    8. Restart Services
                                           ↓
                                    9. Post-Deployment Checks
```

Detailed steps in [SERVER_CONNECTION.md](./SERVER_CONNECTION.md)

## 🆘 Support & Troubleshooting

### Common Issues

**Static files not loading:**
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

**Database connection errors:**
```bash
# Check PostgreSQL service
sudo systemctl status postgresql
```

**Application not starting:**
```bash
# Check logs
sudo journalctl -u gunicorn -n 50
```

See [SERVER_CONNECTION.md](./SERVER_CONNECTION.md) for complete troubleshooting guide.

## 📊 Monitoring

After deployment, monitor:
- Application logs: `sudo journalctl -u gunicorn -f`
- Nginx logs: `sudo tail -f /var/log/nginx/error.log`
- System resources: `htop` or `top`
- Website status: https://goatpedigree.pro

## 🤝 Contributing

When contributing:
1. Create a feature branch
2. Test changes locally
3. Follow the deployment checklist
4. Document any configuration changes

## 📄 License

This project is proprietary software.

## 👥 Team

- Developed by Dkplucas
- Deployed on Oracle Cloud Infrastructure

## 📞 Contact

For deployment issues or questions, refer to the deployment documentation files listed above.

---

**Quick Links:**
- 🚀 [Quick Start Guide](./QUICK_START.md)
- 📖 [Deployment Overview](./DEPLOYMENT_README.md)
- 🔗 [Server Connection Guide](./SERVER_CONNECTION.md)
- ✅ [Deployment Checklist](./DEPLOYMENT_CHECKLIST.md)

**Last Updated:** 2025-01-31  
**Version:** 0.6.1
