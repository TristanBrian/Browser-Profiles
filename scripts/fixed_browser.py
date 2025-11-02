#!/usr/bin/env python3
import sys
import os

# Force Python path to include venv
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
venv_path = os.path.join(project_root, 'browser_env')
venv_site_packages = os.path.join(venv_path, 'lib', 'python3.11', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

print(f"🐍 Python path: {sys.executable}")
print(f"📦 Virtual env: {sys.prefix}")

# Try to import selenium-wire with better error handling
try:
    print("🔄 Importing selenium-wire...")
    from seleniumwire import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    print("✅ SUCCESS: selenium-wire imported!")
    SELENIUM_WIRE_AVAILABLE = True
except ImportError as e:
    print(f"❌ FAILED: {e}")
    print("💡 Try: pip install --force-reinstall selenium-wire")
    sys.exit(1)

import json
import random
import time
import argparse
from urllib.parse import urlparse

class FixedProfileManager:
    def __init__(self, profile_name):
        self.profile_name = profile_name
        self.profiles_dir = os.path.expanduser("~/Documents/browser-profiles")
        self.profile_path = os.path.join(self.profiles_dir, "profiles", profile_name)
        
    def load_profile_config(self):
        config_path = os.path.join(self.profile_path, "config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def get_proxy_config(self):
        config = self.load_profile_config()
        proxy_url = config.get('proxy', '')
        if not proxy_url or proxy_url in ['direct', 'none', '']:
            return None
        return proxy_url
    
    def get_driver(self):
        proxy_url = self.get_proxy_config()
        
        print(f"👤 Profile: {self.profile_name}")
        print(f"🔌 Proxy URL: {proxy_url}")
        
        # Configure Chrome options
        options = Options()
        options.binary_location = "/usr/bin/chromium"
        
        # User data directory
        user_data_dir = os.path.join(self.profile_path, "chrome_data")
        os.makedirs(user_data_dir, exist_ok=True)
        options.add_argument(f"--user-data-dir={user_data_dir}")
        
        # Basic settings
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
        
        # Configure selenium-wire proxy
        seleniumwire_options = {}
        
        if proxy_url:
            parsed = urlparse(proxy_url)
            print(f"🔧 Proxy type: {parsed.scheme.upper()}")
            print(f"🔧 Proxy host: {parsed.hostname}:{parsed.port}")
            
            seleniumwire_options = {
                'proxy': {
                    'http': proxy_url,
                    'https': proxy_url,
                    'no_proxy': 'localhost,127.0.0.1'
                },
                'verify_ssl': False,
                'suppress_connection_errors': False
            }
            print("✅ Using selenium-wire proxy configuration")
        
        try:
            print("🖥️ Starting browser...")
            driver = webdriver.Chrome(
                seleniumwire_options=seleniumwire_options,
                options=options
            )
            
            # Remove automation flags
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver
            
        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            raise

def test_browser():
    print("=" * 60)
    print("🚀 FIXED Browser Test with SOCKS5 Proxy")
    print("=" * 60)
    
    profile_manager = FixedProfileManager("proxy_test")
    
    try:
        driver = profile_manager.get_driver()
        
        # Test multiple URLs
        test_urls = [
            "https://httpbin.org/ip",
            "https://www.google.com",
            "https://ifconfig.me"
        ]
        
        for url in test_urls:
            print(f"\n🌐 Testing: {url}")
            try:
                driver.get(url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                print(f"✅ SUCCESS: {url} loaded")
                print(f"📄 Title: {driver.title}")
                
                # Take screenshot
                screenshot_path = os.path.join(profile_manager.profile_path, f"test_{url.split('//')[1].replace('/', '_')}.png")
                driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot: {screenshot_path}")
                
            except Exception as e:
                print(f"❌ FAILED: {url} - {e}")
        
        print("\n⏎ Press Enter to close browser...")
        input()
        
    except Exception as e:
        print(f"❌ Browser error: {e}")
    finally:
        try:
            driver.quit()
            print("🔒 Browser closed")
        except:
            pass

if __name__ == "__main__":
    test_browser()
