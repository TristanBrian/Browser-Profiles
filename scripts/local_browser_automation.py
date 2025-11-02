#!/usr/bin/env python3
import sys
import os

# Add venv to path if not already activated
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
venv_path = os.path.join(project_root, 'browser_env')

if os.path.exists(venv_path) and venv_path not in sys.prefix:
    site_packages = os.path.join(venv_path, 'lib', 'python3.*', 'site-packages')
    import glob
    site_packages_dirs = glob.glob(site_packages)
    if site_packages_dirs:
        sys.path.insert(0, site_packages_dirs[0])

try:
    # Try selenium-wire first (better proxy support)
    from seleniumwire import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    SELENIUM_WIRE_AVAILABLE = True
except ImportError:
    try:
        # Fall back to regular selenium
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        SELENIUM_WIRE_AVAILABLE = False
        print("⚠️  selenium-wire not available, using regular selenium")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print(f"💡 Install: pip install selenium-wire")
        sys.exit(1)

import json
import random
import time
import argparse
from urllib.parse import urlparse

class LocalProfileManager:
    def __init__(self, profile_name):
        self.profile_name = profile_name
        self.profiles_dir = os.path.expanduser("~/Documents/browser-profiles")
        self.profile_path = os.path.join(self.profiles_dir, "profiles", profile_name)
        os.makedirs(self.profile_path, exist_ok=True)
        
    def load_profile_config(self):
        config_path = os.path.join(self.profile_path, "config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def get_proxy_config(self):
        config = self.load_profile_config()
        proxy_url = config.get('proxy', '')
        if proxy_url in ['direct', 'none', '']:
            return None
        return proxy_url
    
    def generate_fingerprint(self):
        profile_fingerprints = {
            'personal': {
                'user_agents': [
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
                ],
                'screen_resolutions': ["1920x1080", "1366x768"],
                'timezones': ["America/New_York", "Europe/London"]
            }
        }
        
        profile_type = 'personal'
        for p_type in profile_fingerprints:
            if p_type in self.profile_name.lower():
                profile_type = p_type
                break
        
        fingerprints = profile_fingerprints[profile_type]
        
        fingerprint = {
            "user_agent": random.choice(fingerprints['user_agents']),
            "screen_resolution": random.choice(fingerprints['screen_resolutions']),
            "language": "en-US,en;q=0.9",
            "timezone": random.choice(fingerprints['timezones']),
            "profile_type": profile_type
        }
        
        with open(os.path.join(self.profile_path, "fingerprint.json"), 'w') as f:
            json.dump(fingerprint, f, indent=2)
            
        return fingerprint
    
    def get_driver(self, headless=False):
        fingerprint = self.generate_fingerprint()
        proxy_url = self.get_proxy_config()
        
        print(f"👤 Profile: {self.profile_name} ({fingerprint['profile_type']})")
        
        # Configure options
        options = Options()
        options.binary_location = "/usr/bin/chromium"
        
        # User data directory
        user_data_dir = os.path.join(self.profile_path, "chrome_data")
        os.makedirs(user_data_dir, exist_ok=True)
        options.add_argument(f"--user-data-dir={user_data_dir}")
        
        # Anti-detection
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f'--user-agent={fingerprint["user_agent"]}')
        options.add_argument(f'--window-size={fingerprint["screen_resolution"].replace("x", ",")}')
        
        if headless:
            options.add_argument('--headless=new')
        
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Configure proxy based on availability
        seleniumwire_options = {}
        
        if proxy_url:
            print(f"🔌 Using proxy: {proxy_url}")
            
            if SELENIUM_WIRE_AVAILABLE:
                # Use selenium-wire for proper SOCKS5 support
                parsed = urlparse(proxy_url)
                
                seleniumwire_options = {
                    'proxy': {
                        'http': proxy_url,
                        'https': proxy_url,
                        'no_proxy': 'localhost,127.0.0.1'
                    }
                }
                print("✅ Using selenium-wire for proxy support")
                
                try:
                    driver = webdriver.Chrome(
                        seleniumwire_options=seleniumwire_options,
                        options=options
                    )
                except Exception as e:
                    print(f"❌ Selenium-wire failed: {e}")
                    print("🔄 Falling back to regular selenium...")
                    # Fallback to regular selenium
                    options.add_argument(f'--proxy-server={proxy_url}')
                    driver = webdriver.Chrome(options=options)
            else:
                # Regular selenium (may not work with authenticated SOCKS5)
                print("⚠️  Using regular selenium (SOCKS5 auth may not work)")
                options.add_argument(f'--proxy-server={proxy_url}')
                driver = webdriver.Chrome(options=options)
        else:
            print("🌐 No proxy - direct connection")
            driver = webdriver.Chrome(options=options)
        
        # Stealth scripts
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def take_screenshot(self, driver, filename=None):
        if filename is None:
            filename = f"screenshot_{int(time.time())}.png"
        screenshot_path = os.path.join(self.profile_path, filename)
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot: {screenshot_path}")
        return screenshot_path

def test_profile(profile_name, url="https://httpbin.org/ip"):
    print("=" * 60)
    print(f"🚀 Testing Profile: {profile_name}")
    print("=" * 60)
    
    profile_manager = LocalProfileManager(profile_name)
    
    try:
        driver = profile_manager.get_driver(headless=False)
        print(f"🌐 Loading: {url}")
        
        try:
            driver.get(url)
            print("✅ Success! Page loaded")
            print(f"📄 Title: {driver.title}")
            
            # Show some page content
            body = driver.find_element(By.TAG_NAME, "body")
            print(f"📝 Content: {body.text[:200]}...")
            
        except Exception as e:
            print(f"❌ Page load error: {e}")
            print("💡 Trying alternative URL...")
            
            # Try a different URL
            try:
                driver.get("https://www.google.com")
                print("✅ Google loaded successfully!")
                print(f"📄 Title: {driver.title}")
            except Exception as e2:
                print(f"❌ Alternative URL also failed: {e2}")
        
        profile_manager.take_screenshot(driver, f"test_{profile_name}.png")
        
        print("⏎ Press Enter to close...")
        input()
        
    except Exception as e:
        print(f"❌ Browser error: {e}")
    finally:
        try:
            driver.quit()
            print("🔒 Browser closed")
        except:
            pass

def list_profiles():
    profiles_dir = os.path.expanduser("~/Documents/browser-profiles/profiles")
    if os.path.exists(profiles_dir):
        profiles = [d for d in os.listdir(profiles_dir) 
                   if os.path.isdir(os.path.join(profiles_dir, d))]
        print("\n📁 Available Profiles:")
        for profile in profiles:
            config_path = os.path.join(profiles_dir, profile, "config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                proxy = config.get('proxy', 'None')
                print(f"  👤 {profile}: {proxy}")
        return profiles
    return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Browser Profile Automation')
    parser.add_argument('--profile', help='Profile name to use')
    parser.add_argument('--url', default='https://httpbin.org/ip', help='URL to visit')
    parser.add_argument('--list', action='store_true', help='List all profiles')
    parser.add_argument('--setup', action='store_true', help='Run proxy setup')
    
    args = parser.parse_args()
    
    if args.setup:
        os.system("python scripts/setup_proxy.py")
    elif args.list:
        list_profiles()
    elif args.profile:
        test_profile(args.profile, args.url)
    else:
        # Interactive mode
        print("🚀 Browser Profile Automation")
        print("=" * 50)
        
        profiles = list_profiles()
        if profiles:
            print(f"\n🎯 Select a profile to launch:")
            for i, profile in enumerate(profiles, 1):
                config_path = os.path.join(profiles_dir, profile, "config.json")
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    proxy = config.get('proxy', 'Direct')
                    print(f"  {i}. {profile} - {proxy}")
            
            print(f"  {len(profiles)+1}. 🔧 Setup proxy for a profile")
            
            try:
                choice = int(input(f"\nEnter choice (1-{len(profiles)+1}): "))
                
                if 1 <= choice <= len(profiles):
                    selected_profile = profiles[choice-1]
                    print(f"\n🎯 Launching: {selected_profile}")
                    print("-" * 40)
                    test_profile(selected_profile)
                elif choice == len(profiles) + 1:
                    os.system("python scripts/setup_proxy.py")
                else:
                    print("❌ Invalid choice")
                    
            except ValueError:
                print("❌ Please enter a number")
        else:
            print("❌ No profiles found.")

