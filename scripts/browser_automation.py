#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import json
import os
import time
import random
import requests
from typing import Optional, Dict, Any
from urllib.parse import urlparse

class UltimateProfileManager:
    def __init__(self, profile_name: str, hub_url: str = "http://localhost:4444/wd/hub"):
        self.profile_name = profile_name
        self.hub_url = hub_url
        self.profiles_dir = os.path.expanduser("~/Documents/browser-profiles")
        self.profile_path = os.path.join(self.profiles_dir, "profiles", profile_name)
        os.makedirs(self.profile_path, exist_ok=True)
        
    def load_profile_config(self) -> Dict[str, Any]:
        config_path = os.path.join(self.profile_path, "config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def get_proxy_config(self) -> Dict[str, Any]:
        config = self.load_profile_config()
        proxy_url = config.get('proxy', '')
        
        if not proxy_url:
            return {}
        
        try:
            parsed = urlparse(proxy_url)
            return {
                'url': proxy_url,
                'type': parsed.scheme,
                'host': parsed.hostname,
                'port': parsed.port,
                'username': parsed.username,
                'password': parsed.password
            }
        except Exception as e:
            print(f"Error parsing proxy URL: {e}")
            return {}
    
    def test_proxy_connection(self) -> bool:
        proxy_config = self.get_proxy_config()
        
        if not proxy_config:
            print("❌ No proxy configured for this profile")
            return False
        
        proxies = {
            'http': proxy_config['url'],
            'https': proxy_config['url']
        }
        
        try:
            print(f"🔍 Testing proxy: {proxy_config['host']}:{proxy_config['port']}")
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                ip_info = response.json()
                print(f"✅ Proxy working! Your IP: {ip_info.get('origin', 'Unknown')}")
                return True
            else:
                print(f"❌ Proxy test failed with status: {response.status_code}")
                return False
                
        except requests.RequestException as e:
            print(f"❌ Proxy test error: {e}")
            return False
    
    def generate_fingerprint(self) -> Dict[str, Any]:
        user_agents = [
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]
        
        screen_resolutions = ["1920x1080", "1366x768", "1536x864", "1440x900"]
        timezones = ["America/New_York", "Europe/London", "Asia/Tokyo", "Australia/Sydney"]
        
        fingerprint = {
            "user_agent": random.choice(user_agents),
            "screen_resolution": random.choice(screen_resolutions),
            "language": "en-US,en;q=0.9",
            "timezone": random.choice(timezones),
            "hardware_concurrency": random.choice([4, 8, 16]),
            "device_memory": random.choice([4, 8, 16]),
            "platform": random.choice(["Linux x86_64", "Win32", "MacIntel"])
        }
        
        # Save fingerprint
        with open(os.path.join(self.profile_path, "fingerprint.json"), 'w') as f:
            json.dump(fingerprint, f, indent=2)
            
        return fingerprint
    
    def get_driver(self, use_profile_proxy: bool = True, headless: bool = False, timeout: int = 30):
        options = Options()
        fingerprint = self.generate_fingerprint()
        
        # Anti-detection settings
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f'--user-agent={fingerprint["user_agent"]}')
        options.add_argument(f'--window-size={fingerprint["screen_resolution"].replace("x", ",")}')
        
        if headless:
            options.add_argument('--headless=new')
        
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Proxy configuration
        proxy_config = self.get_proxy_config()
        if use_profile_proxy and proxy_config:
            print(f"🔌 Using proxy: {proxy_config['host']}:{proxy_config['port']}")
            options.add_argument(f'--proxy-server={proxy_config["url"]}')
        
        try:
            driver = webdriver.Remote(
                command_executor=self.hub_url,
                options=options
            )
            
            driver.set_page_load_timeout(timeout)
            
            # Stealth modifications
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver
            
        except WebDriverException as e:
            print(f"❌ Error creating driver: {e}")
            print("💡 Try the local version: python3 scripts/local_browser_automation.py")
            raise
    
    def navigate_with_retry(self, driver, url, max_retries: int = 3):
        for attempt in range(max_retries):
            try:
                print(f"🌐 Navigating to {url} (attempt {attempt + 1}/{max_retries})...")
                driver.get(url)
                return True
            except TimeoutException:
                print(f"⏰ Timeout on attempt {attempt + 1}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2)
            except Exception as e:
                print(f"❌ Navigation error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2)
        return False
    
    def take_screenshot(self, driver, filename: str = None):
        if filename is None:
            filename = f"screenshot_{int(time.time())}.png"
        
        screenshot_path = os.path.join(self.profile_path, filename)
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")
        return screenshot_path

def test_browser_automation():
    print("🚀 Testing Browser Automation System...")
    
    profile_manager = UltimateProfileManager("hacking1")
    
    # Test proxy connection first
    print("🔍 Testing proxy connection...")
    profile_manager.test_proxy_connection()
    
    try:
        driver = profile_manager.get_driver(use_profile_proxy=True, headless=False)
        
        print("🌐 Testing browser navigation...")
        profile_manager.navigate_with_retry(driver, "https://httpbin.org/ip")
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        profile_manager.take_screenshot(driver, "test_page.png")
        
        print("✅ Browser automation test successful!")
        print("Press Enter to close browser...")
        input()
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
    
    finally:
        try:
            driver.quit()
            print("🔒 Browser closed.")
        except:
            pass

if __name__ == "__main__":
    test_browser_automation()
