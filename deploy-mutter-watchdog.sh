#!/bin/bash
set -e

echo ">>> Deploying Mutter Watchdog..."

# --- 1. Install Python script ---
echo ">>> Copying Python script to /usr/sbin/"
sudo cp mutter-watchdog.py /usr/sbin/mutter-watchdog.py
sudo chmod 755 /usr/sbin/mutter-watchdog.py

# --- 2. System Service Setup ---
echo ">>> Installing system service"
sudo cp mutter-watchdog-system.service.final /etc/systemd/system/mutter-watchdog.service

echo ">>> Creating system data directory"
sudo mkdir -p /var/lib/mutter-watchdog
sudo chown root:root /var/lib/mutter-watchdog

# --- 3. User Service Setup ---
USER_HOME=$(eval echo ~"$USER")
USER_UNIT_NAME="mutter-watchdog.service"

echo ">>> Installing user service"
mkdir -p "$USER_HOME/.config/systemd/user"
cp mutter-watchdog-user.service "$USER_HOME/.config/systemd/user/$USER_UNIT_NAME"

echo ">>> Creating user data directory"
mkdir -p "$USER_HOME/.local/share/mutter-watchdog"

# --- 4. Reload systemd ---
echo ">>> Reloading systemd"
sudo systemctl daemon-reload
systemctl --user daemon-reload

# --- 5. Enable and start services ---
echo ">>> Enabling and starting system service"
sudo systemctl enable --now mutter-watchdog

echo ">>> Enabling and starting user service"
systemctl --user enable --now mutter-watchdog || echo "⚠️ Enable failed, service will still start but may not persist across reboot."

# --- 6. Done ---
echo "✅ Deployment Complete."
echo "Check status with:"
echo "  sudo systemctl status mutter-watchdog   # System service"
echo "  systemctl --user status mutter-watchdog # User service"
echo "Logs available via journalctl:"
echo "  sudo journalctl -u mutter-watchdog -b"
echo "  journalctl --user -u mutter-watchdog -b"
