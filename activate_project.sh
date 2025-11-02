#!/bin/bash
cd "$(dirname "$0")"
source browser_env/bin/activate
echo "🚀 Virtual environment activated!"
echo "📁 Project directory: $(pwd)"
echo "🐍 Python: $(which python)"
echo "📦 Running from virtual environment"
