🌐 Browser Profile Management System
A comprehensive browser automation and profile management system designed for developers, security researchers, and penetration testers. Manage multiple browser profiles with unique fingerprints, proxy configurations, and automation capabilities.

📋 Table of Contents
Features

System Architecture

Quick Start

Installation

Usage Guide

Profile Management

Proxy Configuration

Browser Automation

Troubleshooting

Security Considerations

API Reference

🚀 Features
Core Capabilities
Multi-Profile Management: Create and manage unlimited browser profiles

SOCKS5/HTTP Proxy Support: Full proxy integration with authentication

Fingerprint Spoofing: Automatic browser fingerprint randomization

Virtual Environment: Isolated Python environment for dependencies

Docker Support: Containerized browser instances (optional)

Persistent Sessions: Separate cookies, history, and settings per profile

Advanced Features
Anti-Detection: Built-in stealth features to avoid automation detection

Profile Templates: Pre-configured profiles for different use cases

Interactive Setup: User-friendly wizard for proxy configuration

Screenshot Capture: Automatic screenshot saving for verification

Cross-Platform: Optimized for Kali Linux and penetration testing workflows

🏗️ System Architecture

browser-profiles/
├── 📁 browser_env/                 # Python virtual environment
├── 📁 scripts/                     # Core automation scripts
│   ├── local_browser_automation.py # Main browser controller
│   ├── profile_manager.sh         # Profile management (Bash)
│   ├── setup_proxy.py             # Interactive proxy setup
│   ├── profile_switcher.py        # Profile management (Python)
│   └── fixed_browser.py           # Enhanced browser with proxy fix
├── 📁 profiles/                    # Profile storage
│   └── 📁 [profile_name]/
│       ├── config.json            # Profile configuration
│       ├── fingerprint.json       # Browser fingerprint data
│       ├── 📁 downloads/          # Download directory
│       ├── 📁 cookies/            # Cookie storage
│       └── 📁 chrome_data/        # Chrome user data
├── 📁 configs/                    # System configuration
│   └── proxies.json               # Proxy database
└── 📄 docker-compose.yml          # Docker configuration

⚡ Quick Start
Prerequisites
Kali Linux (recommended) or other Linux distribution

Python 3.8+

Docker (optional, for containerized mode)

Chromium browser

Basic Setup

# Clone or create the project directory
cd ~/Documents/browser-profiles

# Run the setup script
chmod +x setup_system.sh
./setup_system.sh

# Activate virtual environment
source browser_env/bin/activate

# Create your first profile
./scripts/profile_manager.sh create myprofile 5555

📥 Installation
Step 1: System Dependencies

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3 python3-pip python3-venv chromium chromium-driver docker.io docker-compose

# Add user to docker group (optional)
sudo usermod -aG docker $USER
# Log out and back in for changes to take effect

Step 2: Project Setup

# Navigate to project directory
cd ~/Documents/browser-profiles

# Create virtual environment
python3 -m venv browser_env

# Activate virtual environment
source browser_env/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install selenium requests packaging
pip install selenium-wire blinker==1.7.0

# Verify installation
python -c "from seleniumwire import webdriver; print('✅ Dependencies installed successfully!')"

🎯 Usage Guide
Easy Commands

# Launch browser with profile selection
./browser

# Configure proxies interactively
./proxy-setup

# List all profiles
./profiles --list

# Get quick help
./proxy-help

Profile Management

# Create a new profile
./scripts/profile_manager.sh create work_profile 5556

# Start a profile
./scripts/profile_manager.sh start work_profile

# Stop a profile
./scripts/profile_manager.sh stop work_profile

# List all profiles
./scripts/profile_manager.sh list

# Delete a profile
./scripts/profile_manager.sh delete old_profile

Proxy Configuration

# Interactive proxy setup
python scripts/setup_proxy.py

# Manual proxy configuration
./scripts/profile_manager.sh add-proxy work_profile socks5 192.168.1.100 1080 username password

# Test proxy connection
./scripts/profile_manager.sh test-proxy work_profile

Support
For issues and troubleshooting:

Check the troubleshooting section above

Verify all dependencies are installed

Test proxy connectivity independently

Check file permissions and paths

📄 License
This project is designed for educational and authorized penetration testing purposes only. Users are responsible for complying with all applicable laws and terms of service.

Happy Browsing! 🎉