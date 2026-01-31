#!/usr/bin/env bash
#
# Deployment Verification Script for Goat Pedigree Application
# Run this script on the production server to verify configuration before/after deployment
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/home/goat_app/apps/Goat-Pedigree"
APP_NAME="Goat-Pedigree"
GUNICORN_SERVICE="gunicorn"
NGINX_SERVICE="nginx"

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}Goat Pedigree Deployment Verification${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Function to print info
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if running as the correct user
echo -e "\n${BLUE}[1/10] Checking User${NC}"
CURRENT_USER=$(whoami)
print_info "Running as user: $CURRENT_USER"

# Check system resources
echo -e "\n${BLUE}[2/10] Checking System Resources${NC}"

# Disk space
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 80 ]; then
    print_status 0 "Disk space: ${DISK_USAGE}% used"
else
    print_status 1 "Disk space: ${DISK_USAGE}% used (WARNING: High usage)"
fi

# Memory
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
if [ "$MEMORY_USAGE" -lt 90 ]; then
    print_status 0 "Memory usage: ${MEMORY_USAGE}%"
else
    print_status 1 "Memory usage: ${MEMORY_USAGE}% (WARNING: High usage)"
fi

# Check application directory
echo -e "\n${BLUE}[3/10] Checking Application Directory${NC}"
if [ -d "$APP_DIR" ]; then
    print_status 0 "Application directory exists: $APP_DIR"
    cd "$APP_DIR"
else
    print_status 1 "Application directory not found: $APP_DIR"
    exit 1
fi

# Check git status
echo -e "\n${BLUE}[4/10] Checking Git Status${NC}"
if [ -d ".git" ]; then
    GIT_BRANCH=$(git branch --show-current)
    GIT_COMMIT=$(git rev-parse --short HEAD)
    print_status 0 "Git repository found"
    print_info "Current branch: $GIT_BRANCH"
    print_info "Current commit: $GIT_COMMIT"
    
    # Check for uncommitted changes
    if git diff-index --quiet HEAD --; then
        print_status 0 "No uncommitted changes"
    else
        print_warning "Uncommitted changes detected"
        git status --short
    fi
else
    print_status 1 "Not a git repository"
fi

# Check Python and virtual environment
echo -e "\n${BLUE}[5/10] Checking Python Environment${NC}"
if [ -d "venv" ] || [ -d "env" ] || [ -d ".venv" ]; then
    print_status 0 "Virtual environment found"
else
    print_warning "No virtual environment detected"
fi

PYTHON_VERSION=$(python3 --version 2>&1)
print_info "Python version: $PYTHON_VERSION"

# Check if manage.py exists
if [ -f "manage.py" ]; then
    print_status 0 "Django manage.py found"
else
    print_status 1 "Django manage.py not found"
    exit 1
fi

# Check critical files
echo -e "\n${BLUE}[6/10] Checking Critical Files${NC}"
files_to_check=(
    "requirements.txt"
    "goat_project/settings.py"
    "goat_project/wsgi.py"
    "manage.py"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        print_status 0 "$file exists"
    else
        print_status 1 "$file missing"
    fi
done

# Check directories
echo -e "\n${BLUE}[7/10] Checking Directories and Permissions${NC}"
directories=(
    "media:0755"
    "media/goats:0755"
    "staticfiles:0755"
)

for dir_perm in "${directories[@]}"; do
    IFS=':' read -r dir expected_perm <<< "$dir_perm"
    if [ -d "$dir" ]; then
        ACTUAL_PERM=$(stat -c "%a" "$dir")
        if [ "$ACTUAL_PERM" = "$expected_perm" ]; then
            print_status 0 "$dir exists with correct permissions ($ACTUAL_PERM)"
        else
            print_warning "$dir exists but permissions are $ACTUAL_PERM (expected $expected_perm)"
        fi
    else
        print_status 1 "$dir directory missing"
    fi
done

# Check Django configuration
echo -e "\n${BLUE}[8/10] Checking Django Configuration${NC}"

# Check for DEBUG mode in settings.py
if grep -q "DEBUG = False" goat_project/settings.py; then
    print_status 0 "DEBUG mode is False (production)"
else
    if grep -q "DEBUG = True" goat_project/settings.py; then
        print_status 1 "DEBUG mode is True (WARNING: Should be False in production)"
    else
        print_warning "DEBUG setting not found or uses environment variable"
    fi
fi

# Check for SECRET_KEY
if grep -q "SECRET_KEY" goat_project/settings.py; then
    print_status 0 "SECRET_KEY is configured"
else
    print_status 1 "SECRET_KEY not found"
fi

# Check services status
echo -e "\n${BLUE}[9/10] Checking Services${NC}"

# Check Gunicorn
if systemctl is-active --quiet $GUNICORN_SERVICE 2>/dev/null; then
    print_status 0 "Gunicorn service is running"
else
    print_status 1 "Gunicorn service is not running"
fi

# Check Nginx
if systemctl is-active --quiet $NGINX_SERVICE 2>/dev/null; then
    print_status 0 "Nginx service is running"
else
    print_warning "Nginx service is not running (may not have permission to check)"
fi

# Check PostgreSQL
if systemctl is-active --quiet postgresql 2>/dev/null; then
    print_status 0 "PostgreSQL service is running"
else
    print_warning "PostgreSQL service status unknown (may not have permission to check)"
fi

# Network connectivity check
echo -e "\n${BLUE}[10/10] Checking Network Connectivity${NC}"

# Check if localhost responds
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200\|301\|302"; then
    print_status 0 "Application responds on localhost:8000"
else
    print_warning "Application not responding on localhost:8000"
fi

# Summary
echo -e "\n${BLUE}=====================================${NC}"
echo -e "${BLUE}Verification Complete${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""
print_info "Review the output above for any warnings or errors"
print_info "Check system logs for more details if issues are found:"
echo "  - Gunicorn: sudo journalctl -u gunicorn -n 50"
echo "  - Nginx: sudo tail -f /var/log/nginx/error.log"
echo "  - Application: Check Django logs"
echo ""
