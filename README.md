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
## Dependencies & Troubleshooting

Mutter Watchdog requires a few Python libraries to connect to D-Bus:

- `python3-pydbus`
- `python3-gobject`

### Installing dependencies

On Fedora:
```bash
sudo dnf install python3-pydbus python3-gobject
On Ubuntu/Debian:sudo apt install python3-pydbus python3-gi
On Arch Linux:sudo pacman -S python-pydbus python-gobject

