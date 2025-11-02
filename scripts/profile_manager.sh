#!/bin/bash

PROFILES_DIR="$HOME/Documents/browser-profiles"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"; }
error() { echo -e "${RED}[ERROR] $1${NC}"; }
info() { echo -e "${BLUE}[INFO] $1${NC}"; }

create_profile() {
    local profile_name=$1
    local port=$2
    
    if [[ -z "$profile_name" || -z "$port" ]]; then
        error "Usage: $0 create <profile_name> <port>"
        return 1
    fi
    
    log "Creating profile: $profile_name on port $port"
    
    mkdir -p "$PROFILES_DIR/profiles/$profile_name"
    mkdir -p "$PROFILES_DIR/profiles/$profile_name/downloads"
    mkdir -p "$PROFILES_DIR/profiles/$profile_name/cookies"
    
    # Create profile configuration
    cat > "$PROFILES_DIR/profiles/$profile_name/config.json" << EOL
{
    "profile_name": "$profile_name",
    "port": $port,
    "created": "$(date -Iseconds)",
    "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "screen_resolution": "1920x1080",
    "proxy": "",
    "proxy_type": ""
}
EOL

    # Create individual docker-compose
    cat > "$PROFILES_DIR/docker-compose.$profile_name.yml" << EOL
services:
  $profile_name:
    image: selenium/node-chrome:4.15.0
    container_name: $profile_name
    shm_size: 2gb
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=1
    ports:
      - "$port:4444"
    volumes:
      - $PROFILES_DIR/profiles/$profile_name/downloads:/home/seluser/Downloads
    networks:
      - browser-net

networks:
  browser-net:
    external: true
    name: browser-profiles_browser-net
EOL

    log "Profile $profile_name created successfully!"
}

start_profile() {
    local profile_name=$1
    
    if [[ -z "$profile_name" ]]; then
        error "Usage: $0 start <profile_name>"
        return 1
    fi
    
    if [[ ! -f "$PROFILES_DIR/docker-compose.$profile_name.yml" ]]; then
        error "Profile $profile_name does not exist!"
        return 1
    fi
    
    log "Starting profile: $profile_name"
    
    # Start main stack if not running
    if ! docker network ls | grep -q "browser-profiles_browser-net"; then
        log "Starting main browser stack..."
        cd "$PROFILES_DIR" && docker-compose up -d selenium-hub
        sleep 5
    fi
    
    # Start the profile
    cd "$PROFILES_DIR" && docker-compose -f "docker-compose.$profile_name.yml" up -d
    
    if [[ $? -eq 0 ]]; then
        log "Profile $profile_name started successfully!"
        local port=$(grep -o '"port":[^,]*' "$PROFILES_DIR/profiles/$profile_name/config.json" | cut -d: -f2 | tr -d ' ')
        log "Access via: http://localhost:$port/wd/hub"
    else
        error "Failed to start profile $profile_name"
        log "Try the local version: $0 start-local $profile_name"
    fi
}

start_local_profile() {
    local profile_name=$1
    log "Starting LOCAL profile: $profile_name"
    
    if [[ ! -f "$PROFILES_DIR/profiles/$profile_name/config.json" ]]; then
        error "Profile $profile_name does not exist!"
        return 1
    fi
    
    log "Profile $profile_name ready for local browser use"
    log "Run: python3 $PROFILES_DIR/scripts/local_browser_automation.py"
    log "Or test now? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        python3 "$PROFILES_DIR/scripts/local_browser_automation.py"
    fi
}

stop_profile() {
    local profile_name=$1
    
    if [[ -z "$profile_name" ]]; then
        error "Usage: $0 stop <profile_name>"
        return 1
    fi
    
    log "Stopping profile: $profile_name"
    cd "$PROFILES_DIR" && docker-compose -f "docker-compose.$profile_name.yml" down
    log "Profile $profile_name stopped!"
}

stop_all() {
    log "Stopping all profiles and main stack..."
    cd "$PROFILES_DIR" && docker-compose down
    
    # Stop all individual profiles
    for compose_file in "$PROFILES_DIR"/docker-compose.*.yml; do
        if [[ -f "$compose_file" ]]; then
            profile_name=$(basename "$compose_file" | sed 's/docker-compose\.\(.*\)\.yml/\1/')
            log "Stopping $profile_name..."
            docker-compose -f "$compose_file" down
        fi
    done
    
    log "All profiles stopped!"
}

list_profiles() {
    log "Available profiles:"
    echo "=================="
    
    if ls "$PROFILES_DIR"/profiles/*/config.json >/dev/null 2>&1; then
        for config_file in "$PROFILES_DIR"/profiles/*/config.json; do
            profile_name=$(basename "$(dirname "$config_file")")
            port=$(grep -o '"port":[^,]*' "$config_file" | cut -d: -f2 | tr -d ' ')
            proxy=$(grep -o '"proxy":"[^"]*' "$config_file" | cut -d'"' -f4)
            
            container_id=$(docker ps -q --filter "name=$profile_name")
            status=$([ -n "$container_id" ] && echo "RUNNING" || echo "STOPPED")
            
            echo "Name: $profile_name"
            echo "Port: $port"
            echo "Status: $status"
            echo "Proxy: ${proxy:-None}"
            echo "---"
        done
    else
        echo "No profiles found!"
    fi
}

add_proxy_to_profile() {
    local profile_name=$1
    local proxy_type=$2
    local proxy_host=$3
    local proxy_port=$4
    local proxy_user=$5
    local proxy_pass=$6
    
    if [[ -z "$profile_name" || -z "$proxy_host" || -z "$proxy_port" ]]; then
        error "Usage: $0 add-proxy <profile_name> <type> <host> <port> [username] [password]"
        error "Types: http, https, socks5, socks4"
        return 1
    fi
    
    local config_file="$PROFILES_DIR/profiles/$profile_name/config.json"
    if [[ ! -f "$config_file" ]]; then
        error "Profile $profile_name does not exist!"
        return 1
    fi
    
    # Create proxy configuration
    local proxy_config=""
    if [[ -n "$proxy_user" && -n "$proxy_pass" ]]; then
        proxy_config="$proxy_type://$proxy_user:$proxy_pass@$proxy_host:$proxy_port"
    else
        proxy_config="$proxy_type://$proxy_host:$proxy_port"
    fi
    
    # Update config using Python (since jq might not be installed)
    python3 - <<EOF
import json
import sys

config_file = "$config_file"
proxy_config = "$proxy_config"
proxy_type = "$proxy_type"

try:
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    config['proxy'] = proxy_config
    config['proxy_type'] = proxy_type
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"Proxy added successfully: {proxy_config}")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
EOF
    
    log "Proxy added to profile $profile_name"
}

test_proxy_connection() {
    local profile_name=$1
    
    if [[ -z "$profile_name" ]]; then
        error "Usage: $0 test-proxy <profile_name>"
        return 1
    fi
    
    local config_file="$PROFILES_DIR/profiles/$profile_name/config.json"
    if [[ ! -f "$config_file" ]]; then
        error "Profile $profile_name does not exist!"
        return 1
    fi
    
    local proxy_url=$(grep -o '"proxy":"[^"]*' "$config_file" | cut -d'"' -f4)
    
    if [[ -z "$proxy_url" ]]; then
        error "No proxy configured for profile $profile_name"
        return 1
    fi
    
    log "Testing proxy connection for $profile_name..."
    log "Proxy URL: $proxy_url"
    
    # Test with curl
    if command -v curl &> /dev/null; then
        response=$(curl --max-time 10 --proxy "$proxy_url" -s https://httpbin.org/ip)
        if [[ $? -eq 0 ]]; then
            log "✅ Proxy test successful!"
            echo "Response: $response"
        else
            error "❌ Proxy test failed!"
        fi
    else
        echo "curl not available, cannot test proxy"
    fi
}

case "$1" in
    create)
        create_profile "$2" "$3"
        ;;
    start)
        start_profile "$2"
        ;;
    start-local)
        start_local_profile "$2"
        ;;
    stop)
        stop_profile "$2"
        ;;
    stop-all)
        stop_all
        ;;
    list)
        list_profiles
        ;;
    add-proxy)
        add_proxy_to_profile "$2" "$3" "$4" "$5" "$6" "$7"
        ;;
    test-proxy)
        test_proxy_connection "$2"
        ;;
    *)
        echo "🚀 Browser Profile Management System"
        echo "==================================="
        echo "Commands:"
        echo "  create <name> <port>        - Create new profile"
        echo "  start <name>                - Start profile (Docker)"
        echo "  start-local <name>          - Start profile (Local)"
        echo "  stop <name>                 - Stop profile"
        echo "  stop-all                    - Stop all profiles"
        echo "  list                        - List all profiles"
        echo "  add-proxy <name> <type> <host> <port> [user] [pass] - Add proxy"
        echo "  test-proxy <name>           - Test proxy connection"
        echo ""
        echo "Examples:"
        echo "  $0 create hacking1 5555"
        echo "  $0 add-proxy hacking1 socks5 127.0.0.1 9050"
        echo "  $0 start-local hacking1    (No Docker needed)"
        echo "  $0 test-proxy hacking1"
        echo "  $0 list"
        ;;
esac
