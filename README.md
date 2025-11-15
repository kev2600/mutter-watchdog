# 📖 Mutter Watchdog

Mutter Watchdog is a systemd‑based watchdog for GNOME’s Mutter compositor. It ensures Mutter stays responsive and restarts it if necessary.

The project installs two services:
- System service → runs at boot (pre‑login).
- User service → runs after login (post‑login, inside Wayland).

## 🚀 Quick install

git clone https://github.com/kev2600/mutter-watchdog.git
cd mutter-watchdog
chmod +x deploy-mutter-watchdog.sh
./deploy-mutter-watchdog.sh

## 🔎 Validation

sudo systemctl status mutter-watchdog
systemctl --user status mutter-watchdog
sudo journalctl -u mutter-watchdog -b
journalctl --user -u mutter-watchdog -b

Note: “WATCHDOG: Not a Wayland session” from the system service before login is expected. The user service stays active after login.
