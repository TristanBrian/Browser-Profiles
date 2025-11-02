#!/usr/bin/env python3
import os
import json
import shutil

class ProfileSwitcher:
    def __init__(self):
        self.profiles_dir = os.path.expanduser("~/Documents/browser-profiles/profiles")
    
    def list_profiles(self):
        """List all available profiles"""
        if not os.path.exists(self.profiles_dir):
            print("❌ No profiles directory found")
            return []
        
        profiles = [d for d in os.listdir(self.profiles_dir) 
                   if os.path.isdir(os.path.join(self.profiles_dir, d))]
        
        print("\n📁 Available Profiles:")
        print("=" * 50)
        
        for profile in profiles:
            config_path = os.path.join(self.profiles_dir, profile, "config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                proxy = config.get('proxy', 'None')
                created = config.get('created', 'Unknown')
                
                print(f"👤 {profile}")
                print(f"   📅 Created: {created}")
                print(f"   🔌 Proxy: {proxy}")
                print(f"   💻 Use: python scripts/local_browser_automation.py --profile {profile}")
                print()
        
        return profiles
    
    def create_profile_template(self, name, profile_type="personal"):
        """Create a profile with predefined settings"""
        templates = {
            "personal": {
                "proxy": "",
                "description": "Personal browsing - no proxy"
            },
            "work": {
                "proxy": "http://work-proxy:8080",
                "description": "Work browsing - corporate proxy"
            },
            "shopping": {
                "proxy": "socks5://shopping-proxy:1080", 
                "description": "Shopping - residential proxy"
            },
            "social": {
                "proxy": "socks5://social-proxy:1080",
                "description": "Social media - mobile fingerprint"
            }
        }
        
        template = templates.get(profile_type, templates["personal"])
        
        profile_path = os.path.join(self.profiles_dir, name)
        os.makedirs(profile_path, exist_ok=True)
        os.makedirs(os.path.join(profile_path, "downloads"), exist_ok=True)
        os.makedirs(os.path.join(profile_path, "cookies"), exist_ok=True)
        
        config = {
            "profile_name": name,
            "profile_type": profile_type,
            "description": template["description"],
            "proxy": template["proxy"],
            "created": "2024-01-01T00:00:00"  # Will be updated when used
        }
        
        config_path = os.path.join(profile_path, "config.json")
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Created profile: {name} ({profile_type})")
        return True
    
    def delete_profile(self, name):
        """Delete a profile"""
        profile_path = os.path.join(self.profiles_dir, name)
        if os.path.exists(profile_path):
            shutil.rmtree(profile_path)
            print(f"✅ Deleted profile: {name}")
            return True
        else:
            print(f"❌ Profile not found: {name}")
            return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Profile Management')
    parser.add_argument('--list', action='store_true', help='List all profiles')
    parser.add_argument('--create', help='Create a new profile')
    parser.add_argument('--type', choices=['personal', 'work', 'shopping', 'social'], 
                       default='personal', help='Profile type template')
    parser.add_argument('--delete', help='Delete a profile')
    
    args = parser.parse_args()
    
    switcher = ProfileSwitcher()
    
    if args.list:
        switcher.list_profiles()
    elif args.create:
        switcher.create_profile_template(args.create, args.type)
    elif args.delete:
        switcher.delete_profile(args.delete)
    else:
        # Interactive mode
        switcher.list_profiles()
