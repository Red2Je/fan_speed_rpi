#!/bin/bash
set -e

APP_DIR="/opt/fan-controller"
REPO_URL="https://github.com/Red2Je/fan_speed_rpi"

echo "=== Deploying Fan Control App ==="

# 1. Clone or update repository
if [ -d "$APP_DIR/.git" ]; then
    echo "Updating existing repository..."
    cd $APP_DIR
    git fetch --all
    git reset --hard origin/main
else
    echo "Cloning repository..."
    sudo mkdir -p $APP_DIR
    sudo chown -R $USER:$USER $APP_DIR
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR
fi

# 2. Set up Python virtual environment
if [ ! -d "$APP_DIR/venv" ]; then
    python3 -m venv $APP_DIR/venv
fi
$APP_DIR/venv/bin/pip install -r requirements.txt

# 3. Install and enable systemd service
sudo cp fan_controller.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fan-controller.service
sudo systemctl restart fan-controller.service

echo "=== Deployment Complete! ==="