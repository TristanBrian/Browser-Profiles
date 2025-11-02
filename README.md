# 🌐 Browser Profile Management System

Comprehensive browser automation & profile management system aimed at developers, security researchers, and penetration testers. Manage multiple browser profiles with unique fingerprints, per-profile proxies, and automation capabilities.

---

## 📋 Table of Contents

1. [Features](#-features)
2. [System Architecture](#-system-architecture)
3. [Quick Start](#-quick-start)
4. [Installation](#-installation)
5. [Usage Guide](#-usage-guide)
6. [Profile Management](#-profile-management)
7. [Proxy Configuration](#-proxy-configuration)
8. [Browser Automation](#-browser-automation)
9. [Troubleshooting](#-troubleshooting)
10. [Security Considerations](#-security-considerations)
11. [API Reference](#-api-reference)
12. [License](#-license)

---

# 🚀 Features

## Core Capabilities

* **Multi-Profile Management** — create & manage unlimited browser profiles.
* **SOCKS5 / HTTP Proxy Support** — full proxy integration with authentication.
* **Fingerprint Spoofing** — configurable fingerprint JSON per profile.
* **Virtual Environment** — isolated Python venv for dependencies.
* **Docker Support** — optional containerized browser instances.
* **Persistent Sessions** — separate cookies, history, downloads per profile.

## Advanced Features

* **Anti-Detection** — stealth helpers to reduce automation detection.
* **Profile Templates** — preconfigured templates for different workflows.
* **Interactive Setup** — guided wizard for proxy and profile creation.
* **Screenshot Capture** — automatic verification screenshots.
* **Cross-Platform** — optimized for Kali Linux and pentest workflows.

---

# 🏗️ System Architecture

```
browser-profiles/
├── browser_env/                  # Python virtual environment
├── scripts/                      # Core automation scripts
│   ├── local_browser_automation.py
│   ├── profile_manager.sh
│   ├── setup_proxy.py
│   ├── profile_switcher.py
│   └── fixed_browser.py
├── profiles/                     # Profile storage
│   └── [profile_name]/
│       ├── config.json
│       ├── fingerprint.json
│       ├── downloads/
│       ├── cookies/
│       └── chrome_data/
├── configs/
│   └── proxies.json              # Proxy database
└── docker-compose.yml
```

---

# ⚡ Quick Start

## Prerequisites

* Kali Linux (recommended) or any Linux distro
* Python 3.8+
* Docker (optional)
* Chromium (or Chrome)

## Basic Setup

```bash
# Create project directory
cd ~/Documents
git clone <your-repo-url> browser-profiles
cd browser-profiles

# Make setup script executable and run
chmod +x setup_system.sh
./setup_system.sh

# Activate virtual environment
source browser_env/bin/activate

# Create your first profile (example)
./scripts/profile_manager.sh create myprofile 5555
```

---

# 📥 Installation

## Step 1 — System Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv chromium chromium-driver docker.io docker-compose
sudo usermod -aG docker $USER   # optional: add user to docker group
# NOTE: log out and back in for docker group to take effect
```

## Step 2 — Project Setup

```bash
cd ~/Documents/browser-profiles

# Create and activate venv
python3 -m venv browser_env
source browser_env/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install selenium requests packaging selenium-wire blinker==1.7.0

# Quick verify
python -c "from seleniumwire import webdriver; print('✅ Dependencies installed successfully!')"
```

---

# 🎯 Usage Guide

## CLI Shortcuts

```bash
# Launch browser with profile selection
./browser

# Configure proxies interactively
./proxy-setup

# List all profiles
./profiles --list

# Quick help for proxy usage
./proxy-help
```

---

# 🧭 Profile Management

## Common Commands (profile_manager.sh)

```bash
# Create a profile
./scripts/profile_manager.sh create work_profile 5556

# Start a profile (launch browser instance)
./scripts/profile_manager.sh start work_profile

# Stop a profile
./scripts/profile_manager.sh stop work_profile

# List all profiles
./scripts/profile_manager.sh list

# Delete a profile
./scripts/profile_manager.sh delete old_profile
```

## Example `config.json` (per profile)

```json
{
  "name": "work_profile",
  "port": 5556,
  "proxy": {
    "type": "socks5",
    "host": "192.168.1.100",
    "port": 1080,
    "username": "user",
    "password": "pass"
  },
  "fingerprint_file": "fingerprint.json",
  "downloads_dir": "downloads",
  "cookies_dir": "cookies",
  "chrome_user_data": "chrome_data"
}
```

---

# 🌐 Proxy Configuration

## Interactive

```bash
python scripts/setup_proxy.py
```

## Manual (via script)

```bash
./scripts/profile_manager.sh add-proxy work_profile socks5 192.168.1.100 1080 username password
```

## Test a proxy

```bash
./scripts/profile_manager.sh test-proxy work_profile
```

## Example `proxies.json` (configs/proxies.json)

```json
[
  {
    "id": "proxy-1",
    "type": "socks5",
    "host": "192.168.1.100",
    "port": 1080,
    "username": "user",
    "password": "pass",
    "tags": ["fast", "us-east"]
  }
]
```

---

# 🤖 Browser Automation

* `local_browser_automation.py` — entry point for launching Chromium with Selenium/Selenium-Wire, applying profile config, fingerprint, and proxy.
* `fixed_browser.py` — contains enhancements to handle proxy authentication popups and WebRTC/IP leak mitigations.
* `profile_switcher.py` — helper to swap Chrome user-data directories and start the right profile instance.

## Example automation snippet (Selenium + Selenium-Wire)

```python
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--user-data-dir=/path/to/profile/chrome_data")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--no-sandbox")

seleniumwire_options = {
    'proxy': {
        'http': 'socks5://user:pass@192.168.1.100:1080',
        'https': 'socks5://user:pass@192.168.1.100:1080',
        'no_proxy': 'localhost,127.0.0.1'
    }
}

driver = webdriver.Chrome(options=opts, seleniumwire_options=seleniumwire_options)
driver.get("https://example.com")
```

---

# 🛠️ Troubleshooting

* **Chromium won't launch**: confirm `chromium-driver` version matches browser version.
* **Proxy authentication fails**: test proxy with `curl` or `proxy-setup` tool.
* **Permissions**: ensure profile directories are owned by your user.
* **Docker mode**: map host ports and mount profile volume in `docker-compose.yml`.
* **Selenium errors**: run automation script in verbose/log mode to capture stack trace.

---

# 🔐 Security Considerations

* Use this system **only** for authorized testing or educational purposes.
* Never use automated fingerprinting & proxying to bypass law, terms of service, or to perform fraud.
* Keep sensitive credentials out of repo — use environment variables or an encrypted vault.
* Limit access to profile directories and proxy configuration files (chmod 700 where appropriate).
* Be careful with shared machines — avoid storing persistent credentials in `chrome_data` if machine is multi-user.

---

# ⚙️ API Reference (quick)

* `scripts/profile_manager.sh create <name> <port>` — create profile
* `scripts/profile_manager.sh start <name>` — start profile browser
* `scripts/profile_manager.sh stop <name>` — stop profile browser
* `scripts/profile_manager.sh add-proxy <name> <type> <host> <port> [user] [pass]` — attach proxy
* `scripts/profile_manager.sh test-proxy <name>` — run quick proxy connectivity test

---

# 📄 License

This project is intended for **educational and authorized penetration testing** only. Users are responsible for complying with all applicable laws and terms of service.

---

Happy Browsing! 🎉
