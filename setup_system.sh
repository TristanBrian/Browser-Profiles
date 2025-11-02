#!/bin/bash

echo "🚀 Setting up Ultimate Browser Profile Management System..."
echo "=========================================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[SETUP] $1${NC}"; }
error() { echo -e "${RED}[ERROR] $1${NC}"; }

# Check Docker
if ! command -v docker &> /dev/null; then
    log "Installing Docker..."
    sudo apt update
    sudo apt install -y docker.io
    sudo systemctl enable docker --now
    sudo usermod -aG docker $USER
    log "Docker installed. Please log out and back in."
fi

# Create directory structure
log "Creating directory structure..."
mkdir -p ~/browser-profiles/{scripts,profiles,configs}

# Create main docker-compose
cat > ~/browser-profiles/docker-compose.yml << 'EOF'
version: '3.8'
services:
  selenium-hub:
    image: seleniarm/hub:latest
    container_name: selenium-hub
    ports:
      - "4444:4444"
    networks:
      - browser-net

  chrome-profile-base:
    image: seleniarm/node-chromium:latest
    shm_size: 2gb
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=5
      - SE_NODE_OVERRIDE_MAX_SESSIONS=true
    networks:
      - browser-net
    profiles:
      - base

networks:
  browser-net:
    driver: bridge
EOF

log "Setup complete! 🎉"
echo ""
echo "Next: Create the script files below"
