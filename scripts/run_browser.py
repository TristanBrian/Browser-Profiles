#!/usr/bin/env python3
import os
import sys

# Add the virtual environment to the path
venv_path = os.path.join(os.path.dirname(__file__), 'browser_env')
if os.path.exists(venv_path):
    # Add venv site-packages to Python path
    site_packages = os.path.join(venv_path, 'lib', 'python3.*', 'site-packages')
    import glob
    site_packages_dirs = glob.glob(site_packages)
    if site_packages_dirs:
        sys.path.insert(0, site_packages_dirs[0])
    
    # Set Python path to use venv
    python_bin = os.path.join(venv_path, 'bin', 'python')
    if os.path.exists(python_bin):
        os.environ['PYTHONPATH'] = ':'.join(sys.path)

# Now import and run the actual script
from scripts.local_browser_automation import test_local_browser

if __name__ == "__main__":
    test_local_browser()
