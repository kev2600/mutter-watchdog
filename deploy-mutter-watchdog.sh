#!/bin/bash
# FINAL Distro-Agnostic Deployment Script (Wrapper Eliminated)

# --- 1. CONFIGURATION ---
UNIT_FILE_SOURCE="mutter-watchdog@.service.final"
UNIT_FILE_DEST="/etc/systemd/user/"
SERVICE_NAME="mutter-watchdog@$(whoami).service"
SYSTEM_SERVICE="mutter-watchdog.service"

echo "--- STARTING ULTIMATE MUTTER WATCHDOG DEPLOYMENT ---"

# --- 2. DYNAMIC DEPENDENCY INSTALLATION ---

echo "2.1. Installing global Python dependency (python3-pydbus)..."
if command -v dnf &> /dev/null; then
    sudo dnf install -y python3-pydbus
elif command -v apt &> /dev/null; then
    sudo apt update
    sudo apt install -y python3-pydbus
elif command -v pacman &> /dev/null; then
    sudo pacman -Sy python-pydbus
else
    echo "WARNING: Could not detect known package manager. Please install 'python3-pydbus' manually."
fi

# --- 3. CLEANUP & DEPLOYMENT OF UNIT FILE ---

echo "3.1. Disabling old, failing system service: $SYSTEM_SERVICE"
sudo systemctl disable --now "$SYSTEM_SERVICE" || true

echo "3.2. Deploying final unit file to $UNIT_FILE_DEST"
# Copy the provided unit file to the system location
sudo cp "$UNIT_FILE_SOURCE" "$UNIT_FILE_DEST/mutter-watchdog@.service"

# --- 4. SERVICE ACTIVATION & PERSISTENCE ---

echo "4.1. Reloading systemd to find the new unit file..."
systemctl --user daemon-reload

echo "4.2. Enabling and RESTARTING the service: $SERVICE_NAME"
# CRITICAL FIX: Use 'restart' to ensure the service loads the new config,
# even if it was already running.
systemctl --user enable "$SERVICE_NAME"
systemctl --user restart "$SERVICE_NAME"

# --- 5. FINAL VERIFICATION ---

echo "5.1. Verifying service status..."
systemctl --user status "$SERVICE_NAME" | head -n 12

echo "--- DEPLOYMENT COMPLETE ---"
