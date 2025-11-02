#!/bin/bash

PROFILES_DIR="$HOME/Documents/browser-profiles"

echo "🚀 Quick Proxy Setup"
echo "===================="

# List profiles
echo "📁 Available profiles:"
find "$PROFILES_DIR/profiles" -name "config.json" -type f | while read config; do
    profile=$(basename $(dirname "$config"))
    proxy=$(grep -o '"proxy":"[^"]*' "$config" | cut -d'"' -f4)
    echo "  👤 $profile: ${proxy:-Direct}"
done

echo ""
echo "🎯 Quick Commands:"
echo "  python scripts/setup_proxy.py          - Interactive proxy setup"
echo "  python scripts/local_browser_automation.py --list  - List & use profiles"
echo ""
echo "🔧 Manual proxy setup:"
echo "  ./scripts/profile_manager.sh add-proxy <profile> <type> <host> <port> [user] [pass]"
echo ""
echo "Example:"
echo "  ./scripts/profile_manager.sh add-proxy hacking1 socks5 192.168.1.100 1080 myuser mypass"
