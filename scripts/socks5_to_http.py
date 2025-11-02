#!/usr/bin/env python3
"""
Quick script to test if we can use socks5 proxies via HTTP bridge
"""
import requests
from urllib.parse import urlparse

def test_socks5_via_http(proxy_url, test_url="https://httpbin.org/ip"):
    """
    Try different methods to use SOCKS5 proxy
    """
    parsed = urlparse(proxy_url)
    
    print(f"🔧 Testing SOCKS5 proxy: {parsed.hostname}:{parsed.port}")
    
    # Method 1: Direct SOCKS5 with requests
    try:
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        response = requests.get(test_url, proxies=proxies, timeout=10)
        print(f"✅ Method 1 (direct) - IP: {response.json().get('origin')}")
    except Exception as e:
        print(f"❌ Method 1 failed: {e}")
    
    # Method 2: Using socks5h scheme (DNS resolution through proxy)
    try:
        socks5h_url = proxy_url.replace('socks5://', 'socks5h://')
        proxies = {
            'http': socks5h_url,
            'https': socks5h_url
        }
        response = requests.get(test_url, proxies=proxies, timeout=10)
        print(f"✅ Method 2 (socks5h) - IP: {response.json().get('origin')}")
    except Exception as e:
        print(f"❌ Method 2 failed: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_socks5_via_http(sys.argv[1])
    else:
        print("Usage: python socks5_to_http.py <socks5_proxy_url>")
