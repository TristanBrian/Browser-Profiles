Browser Profiles - Multi-proxy automation
========================================

Quick start:
1. Run setup:
   bash ~/browser-profiles/setup_system.sh

2. Start Selenium hub:
   cd ~/browser-profiles
   docker-compose up -d selenium-hub

3. Create profiles:
   ~/browser-profiles/scripts/profile_manager.sh create hacking1 5555
   ~/browser-profiles/scripts/profile_manager.sh create hacking2 5556

4. Add proxies to profiles:
   ~/browser-profiles/scripts/profile_manager.sh add-proxy hacking1 socks5 127.0.0.1 9050
   ~/browser-profiles/scripts/profile_manager.sh add-proxy hacking2 http 192.168.1.100 8080 user pass

5. Start profile containers:
   ~/browser-profiles/scripts/profile_manager.sh start hacking1
   ~/browser-profiles/scripts/profile_manager.sh start hacking2

6. Test via browser automation:
   python3 ~/browser-profiles/scripts/browser_automation.py hacking1

Notes:
- Use proxy_manager.py for maintaining and testing large proxy pools:
  python3 ~/browser-profiles/scripts/proxy_manager.py --test-all
  python3 ~/browser-profiles/scripts/proxy_manager.py --list-working

Security & Ethics:
- Do not use these tools to access accounts, data, or services without permission.
- Do not attempt to bypass security, CAPTCHAs, or access restrictions in ways that violate laws or terms of service.
