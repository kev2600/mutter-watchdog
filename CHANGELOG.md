# 📌 Changelog

All notable changes to **Mutter Watchdog** will be documented here.

---

## [v1.1.0] - 2025-11-14
### Added
- Unified deploy script (`deploy-mutter-watchdog.sh`) for cross‑distro installation
- Automatic setup of both system and user services
- Creation of required data directories
- Clear post‑install validation instructions

### Changed
- Polished `README.md` with Quick Install and dual‑service overview
- Simplified installation workflow (one‑shot deploy script replaces manual steps)

### Notes
- System service logs “WATCHDOG: Not a Wayland session” before login — this is expected
- User service stays active after login in Wayland session
- Tested successfully on Fedora, Ubuntu, Arch

---

## [v1.0.0] - Initial release
- Basic watchdog Python script
- Manual systemd unit setup
