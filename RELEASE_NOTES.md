# 🚀 Mutter Watchdog v1.1.0 Release Notes

## Highlights
- **Unified Deploy Script**  
  New `deploy-mutter-watchdog.sh` automates installation across distros in one command.
- **Dual Service Setup**  
  Handles both system (pre‑login) and user (post‑login) services automatically.
- **Data Directories**  
  Creates required directories under `/var/lib/mutter-watchdog` and `~/.local/share/mutter-watchdog`.
- **Improved Documentation**  
  Polished `README.md` with Quick Install, validation steps, and expected behavior.

## Changes
- Simplified installation workflow (no manual copying of unit files required).
- Clearer instructions for validating services and logs.
- Release notes and changelog added for professional version tracking.

## Known Behavior
- System service may log:

EOFlappy@fedora:~/mutter-watchdog$ git add README.md
git commit -m "Update README with quick install and dual-service instructions"
[main c9670a2] Update README with quick install and dual-service instructions
 1 file changed, 16 insertions(+), 54 deletions(-)
lappy@fedora:~/mutter-watchdog$ git push origin main
Username for 'https://github.com': kev2600
Password for 'https://kev2600@github.com': 
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 735 bytes | 367.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/kev2600/mutter-watchdog.git
   65e77c1..c9670a2  main -> main
lappy@fedora:~/mutter-watchdog$ 
lappy@fedora:~/mutter-watchdog$ tee CHANGELOG.md <<'EOF'
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
