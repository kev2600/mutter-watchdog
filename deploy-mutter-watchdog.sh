#!/bin/bash

# --- 1. SYSTEM SERVICE DEPLOYMENT (GDM Monitor) ---
# Runs as root, starts early, and uses a system-wide data directory.

# --- 0. Copy Main Python Script to Executable Location ---
echo "0. Copying main Python script to /usr/sbin/..."
sudo cp mutter-watchdog.py /usr/sbin/mutter-watchdog.py
sudo chmod +x /usr/sbin/mutter-watchdog.py

echo "--- 1. Deploying System Service (GDM/Boot Monitor) ---"

SYSTEM_UNIT_NAME="mutter-watchdog-system.service"
# ... rest of the script continues below ...

SYSTEM_UNIT_NAME="mutter-watchdog-system.service"
SYSTEM_UNIT_FILE="mutter-watchdog-system.service.final"

# 1a. Create the required system data directory if it doesn't exist
sudo mkdir -p /var/lib/mutter-watchdog
sudo chown root:root /var/lib/mutter-watchdog
sudo chmod 755 /var/lib/mutter-watchdog

# 1b. Copy and enable the System Service unit file
sudo cp "$SYSTEM_UNIT_FILE" "/etc/systemd/system/$SYSTEM_UNIT_NAME"
sudo chmod 644 "/etc/systemd/system/$SYSTEM_UNIT_NAME"

sudo systemctl daemon-reload
sudo systemctl enable "$SYSTEM_UNIT_NAME"

echo "✅ System Service ($SYSTEM_UNIT_NAME) deployed and enabled for boot."
echo "   This monitors pre-login (GDM) crashes."
echo "---"

# --- 2. USER SERVICE DEPLOYMENT (Session Monitor) ---
# Runs as the current user, starts after login, and uses the user's $HOME/.config directory.

echo "--- 2. Deploying User Service (Session Monitor) ---"

USER_UNIT_NAME="mutter-watchdog-user.service"
USER_UNIT_FILE="mutter-watchdog-user.service.final"

# Get the current non-root user's home directory path
if [ "$SUDO_USER" ]; then
    USER_HOME=$(eval echo "~$SUDO_USER")
else
    USER_HOME=$HOME
fi
USER_CONFIG_DIR="$USER_HOME/.config/systemd/user"

echo "Deploying User Service to $USER_CONFIG_DIR..."

# 2a. Ensure the user's systemd directory exists
mkdir -p "$USER_CONFIG_DIR"

# 2b. Copy the User Service unit file
cp "$USER_UNIT_FILE" "$USER_CONFIG_DIR/$USER_UNIT_NAME"

# 2c. Create the User's data directory for the SQLite DB
mkdir -p "$USER_HOME/.config/mutter-watchdog"

echo "✅ User Service ($USER_UNIT_NAME) unit file deployed to user configuration."
echo "---"

# --- 3. ACTIVATION INSTRUCTIONS ---

echo "Deployment Complete."
echo "---"
echo "To activate the User Service (post-login monitor) and make it persistent, run:"
echo "systemctl --user daemon-reload"
echo "systemctl --user start $USER_UNIT_NAME"
echo " "
echo "Since the 'enable' command can fail on some distributions, you must ensure the service starts at boot via your desktop's 'Startup Applications' tool or other user-specific autostart methods."
