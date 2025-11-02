#!/usr/bin/env python3
import json
import os
import requests
from typing import List, Dict, Any

class ProxyManager:
    def __init__(self, profiles_dir: str = "~/browser-profiles"):
        self.profiles_dir = os.path.expanduser(profiles_dir)
        self.proxies_file = os.path.join(self.profiles_dir, "configs", "proxies.json")
        os.makedirs(os.path.dirname(self.proxies_file), exist_ok=True)
        self.load_proxies()
    
    def load_proxies(self):
        if os.path.exists(self.proxies_file):
            with open(self.proxies_file, 'r') as f:
                self.proxies = json.load(f)
        else:
            self.proxies = {
                "http_proxies": [],
                "socks5_proxies": [],
                "socks4_proxies": []
            }
    
    def save_proxies(self):
        with open(self.proxies_file, 'w') as f:
            json.dump(self.proxies, f, indent=2)
    
    def add_proxy(self, proxy_type: str, host: str, port: int, 
                  username: str = None, password: str = None):
        proxy_data = {
            "host": host,
            "port": port,
            "username": username,
            "password": password,
            "working": True
        }
        
        # Clean empty fields
        proxy_data = {k: v for k, v in proxy_data.items() if v is not None}
        
        if proxy_type in self.proxies:
            self.proxies[proxy_type].append(proxy_data)
        else:
            self.proxies[proxy_type] = [proxy_data]
        
        self.save_proxies()
        print(f"✅ Added {proxy_type} proxy: {host}:{port}")
    
    def test_proxy(self, proxy_type: str, proxy_data: Dict) -> bool:
        try:
            if proxy_data.get('username') and proxy_data.get('password'):
                proxy_url = f"{proxy_type}://{proxy_data['username']}:{proxy_data['password']}@{proxy_data['host']}:{proxy_data['port']}"
            else:
                proxy_url = f"{proxy_type}://{proxy_data['host']}:{proxy_data['port']}"
            
            proxies = {'http': proxy_url, 'https': proxy_url}
            response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Proxy working - IP: {response.json().get('origin', 'Unknown')}")
                return True
            return False
        except Exception as e:
            print(f"❌ Proxy test error: {e}")
            return False
    
    def test_all_proxies(self):
        print("🔍 Testing all proxies...")
        
        for proxy_type, proxy_list in self.proxies.items():
            print(f"\nTesting {proxy_type}:")
            for proxy in proxy_list:
                print(f"  Testing {proxy['host']}:{proxy['port']}...", end=" ")
                proxy['working'] = self.test_proxy(proxy_type, proxy)
        
        self.save_proxies()
        print("\n✅ All proxies tested!")
    
    def get_working_proxies(self, proxy_type: str = None):
        working_proxies = []
        
        if proxy_type:
            proxy_types = [proxy_type]
        else:
            proxy_types = self.proxies.keys()
        
        for p_type in proxy_types:
            if p_type in self.proxies:
                working_proxies.extend([
                    proxy for proxy in self.proxies[p_type] 
                    if proxy.get('working', False)
                ])
        
        return working_proxies

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Proxy Management System")
    subparsers = parser.add_subparsers(dest='command')
    
    add_parser = subparsers.add_parser('add', help='Add proxy')
    add_parser.add_argument('type', choices=['http_proxies', 'socks5_proxies', 'socks4_proxies'])
    add_parser.add_argument('host', help='Proxy host')
    add_parser.add_argument('port', type=int, help='Proxy port')
    add_parser.add_argument('--username', help='Username')
    add_parser.add_argument('--password', help='Password')
    
    subparsers.add_parser('test', help='Test all proxies')
    subparsers.add_parser('list', help='List proxies')
    
    args = parser.parse_args()
    proxy_manager = ProxyManager()
    
    if args.command == 'add':
        proxy_manager.add_proxy(args.type, args.host, args.port, args.username, args.password)
    elif args.command == 'test':
        proxy_manager.test_all_proxies()
    elif args.command == 'list':
        print(json.dumps(proxy_manager.proxies, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
