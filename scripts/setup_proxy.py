#!/usr/bin/env python3
import os
import json
import sys

def setup_proxy_interactive():
    print("🎯 Proxy Setup Wizard")
    print("=" * 50)
    
    profiles_dir = os.path.expanduser("~/Documents/browser-profiles/profiles")
    
    # List available profiles
    profiles = [d for d in os.listdir(profiles_dir) 
               if os.path.isdir(os.path.join(profiles_dir, d))]
    
    if not profiles:
        print("❌ No profiles found. Create one first.")
        return
    
    print("\n📁 Available Profiles:")
    for i, profile in enumerate(profiles, 1):
        print(f"  {i}. {profile}")
    
    try:
        choice = int(input(f"\nSelect profile (1-{len(profiles)}): ")) - 1
        if 0 <= choice < len(profiles):
            profile_name = profiles[choice]
        else:
            print("❌ Invalid choice")
            return
    except ValueError:
        print("❌ Please enter a number")
        return
    
    profile_path = os.path.join(profiles_dir, profile_name)
    config_path = os.path.join(profile_path, "config.json")
    
    # Load existing config
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    
    print(f"\n🔧 Configuring proxy for: {profile_name}")
    print("\n🔌 Proxy Types:")
    print("1. SOCKS5")
    print("2. HTTP/HTTPS") 
    print("3. No proxy (direct connection)")
    print("4. Remove existing proxy")
    
    try:
        proxy_choice = int(input("\nSelect proxy type (1-4): "))
    except ValueError:
        print("❌ Please enter a number")
        return
    
    if proxy_choice == 1:
        # SOCKS5
        print("\n🔄 SOCKS5 Proxy Setup")
        host = input("Host (e.g., 192.168.1.100 or proxy.example.com): ").strip()
        port = input("Port (e.g., 1080): ").strip()
        username = input("Username (leave empty if none): ").strip()
        password = input("Password (leave empty if none): ").strip()
        
        if username and password:
            proxy_url = f"socks5://{username}:{password}@{host}:{port}"
        else:
            proxy_url = f"socks5://{host}:{port}"
        
        config['proxy'] = proxy_url
        config['proxy_type'] = 'socks5'
        
    elif proxy_choice == 2:
        # HTTP/HTTPS
        print("\n🌐 HTTP/HTTPS Proxy Setup")
        host = input("Host (e.g., 192.168.1.100 or proxy.example.com): ").strip()
        port = input("Port (e.g., 8080): ").strip()
        username = input("Username (leave empty if none): ").strip()
        password = input("Password (leave empty if none): ").strip()
        
        if username and password:
            proxy_url = f"http://{username}:{password}@{host}:{port}"
        else:
            proxy_url = f"http://{host}:{port}"
        
        config['proxy'] = proxy_url
        config['proxy_type'] = 'http'
        
    elif proxy_choice == 3:
        # No proxy
        config['proxy'] = ''
        config['proxy_type'] = 'direct'
        print("✅ Set to direct connection (no proxy)")
        
    elif proxy_choice == 4:
        # Remove proxy
        config['proxy'] = ''
        config['proxy_type'] = ''
        print("✅ Proxy removed")
        
    else:
        print("❌ Invalid choice")
        return
    
    # Save config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Profile '{profile_name}' updated!")
    print(f"🔌 Proxy: {config.get('proxy', 'None')}")
    
    # Test the proxy
    if config.get('proxy'):
        test = input("\n🧪 Test proxy connection now? (y/N): ").strip().lower()
        if test == 'y':
            test_proxy_connection(profile_name)

def test_proxy_connection(profile_name):
    """Test the proxy connection"""
    import requests
    from urllib.parse import urlparse
    
    profiles_dir = os.path.expanduser("~/Documents/browser-profiles/profiles")
    config_path = os.path.join(profiles_dir, profile_name, "config.json")
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        proxy_url = config.get('proxy', '')
        
        if proxy_url:
            print(f"\n🔍 Testing proxy: {proxy_url}")
            
            try:
                proxies = {
                    'http': proxy_url,
                    'https': proxy_url
                }
                response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
                
                if response.status_code == 200:
                    ip_info = response.json()
                    print(f"✅ Proxy WORKING!")
                    print(f"🌐 Your IP: {ip_info.get('origin', 'Unknown')}")
                else:
                    print(f"❌ Proxy failed - Status: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Proxy test error: {e}")
        else:
            print("ℹ️ No proxy configured")
    else:
        print("❌ Profile config not found")

if __name__ == "__main__":
    setup_proxy_interactive()
