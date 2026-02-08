#!/usr/bin/env bash
#
# Quick deployment script for Goat Pedigree
# This script automates the basic deployment steps
# Run this ON THE SERVER after SSH connection
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}   Goat Pedigree Quick Deploy${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

APP_DIR="/home/goat_app/apps/Goat-Pedigree"

# Ensure we're in the correct directory
if [ ! -d "$APP_DIR" ]; then
    echo -e "${RED}Error: Application directory not found: $APP_DIR${NC}"
    exit 1
fi

cd "$APP_DIR"

# Step 1: Check current status
echo -e "${BLUE}[1/8] Checking current status...${NC}"
git status
echo ""

# Step 2: Backup database
echo -e "${BLUE}[2/8] Backing up database...${NC}"
BACKUP_FILE=~/backup_$(date +%Y%m%d_%H%M%S).sql
echo "Creating backup: $BACKUP_FILE"
sudo -u postgres pg_dump goatpedigreedb > "$BACKUP_FILE" || echo -e "${YELLOW}Warning: Could not create database backup${NC}"
echo -e "${GREEN}✓ Backup created${NC}"
echo ""

# Step 3: Pull latest changes
echo -e "${BLUE}[3/8] Pulling latest changes...${NC}"
read -p "Enter branch name (default: main): " BRANCH
BRANCH=${BRANCH:-main}
git fetch origin
git pull origin "$BRANCH"
echo -e "${GREEN}✓ Code updated${NC}"
echo ""

# Step 4: Activate virtual environment
echo -e "${BLUE}[4/8] Activating virtual environment...${NC}"
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment activated (venv)${NC}"
elif [ -d "env" ]; then
    source env/bin/activate
    echo -e "${GREEN}✓ Virtual environment activated (env)${NC}"
else
    echo -e "${YELLOW}Warning: No virtual environment found${NC}"
fi
echo ""

# Step 5: Install dependencies
echo -e "${BLUE}[5/8] Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 6: Run migrations
echo -e "${BLUE}[6/8] Running database migrations...${NC}"
python manage.py migrate --plan
python manage.py migrate
echo -e "${GREEN}✓ Migrations applied${NC}"
echo ""

# Step 7: Collect static files
echo -e "${BLUE}[7/8] Collecting static files...${NC}"
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Static files collected${NC}"
echo ""

# Step 8: Restart services
echo -e "${BLUE}[8/8] Restarting services...${NC}"
sudo systemctl restart gunicorn
echo "Waiting for Gunicorn to start..."
sleep 3

if systemctl is-active --quiet gunicorn; then
    echo -e "${GREEN}✓ Gunicorn restarted successfully${NC}"
else
    echo -e "${RED}✗ Gunicorn failed to start${NC}"
    echo "Check logs with: sudo journalctl -u gunicorn -n 50"
    exit 1
fi
echo ""

# Final check
echo -e "${BLUE}======================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo "Next steps:"
echo "1. Run verification: ./verify_deployment.sh"
echo "2. Check logs: sudo journalctl -u gunicorn -f"
echo "3. Test website: https://goatpedigree.pro"
echo ""
echo "Backup location: $BACKUP_FILE"
echo ""
