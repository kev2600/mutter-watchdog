# NVIDIA Wayland Stability Toolkit: Complete Fix (Package v1.0)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This repository contains the complete, self-contained **NVIDIA Wayland Stability Toolkit**.

---

## 💡 Purpose: A Powerful Missing Layer for Stability

The NVIDIA Wayland Stability Toolkit acts as a **powerful missing layer**  to **mitigate** display instability and provide a **recoverable style** of operation in NVIDIA Wayland/Mutter environments.

This package provides a set of services that soft-contain stability issues by:
1.  **Continuous Monitoring:** Tracking critical events such as NVIDIA driver changes, screen disconnects, and session transitions.
2.  **State Recovery:** Automatically and reliably reapplying your correct screen resolution and display settings to maintain a stable, consistent desktop state.

This package also resolves two key deployment issues that prevented the original toolkit from functioning correctly on modern Linux distributions:
* The "unable to open database file" startup error.
* Security context errors (e.g., status 216/GROUP) by ensuring correct deployment as a systemd user service.

## 🛠️ Prerequisites

This package is self-contained. The only prerequisite is that your system must be running:
* A modern Linux distribution (using `systemd`).
* A user session with a D-Bus environment.

## 🚀 Deployment Instructions

The repository includes a robust installer script (`deploy-mutter-watchdog.sh`) that handles dependencies and service management.

### 1. Download and Extract

Clone the repository or download the final compressed archive: `mutter-watchdog-full-toolkit.tar.gz`.

# Example for extracting the archive
tar -xzvf mutter-watchdog-full-toolkit.tar.gz

2. Run the Installer (deploy-mutter-watchdog.sh)
The installer will copy the core script (mutter-watchdog.py), deploy the fixed unit file, check for the required Python dependencies (python3-pydbus), and activate the service.


3. Verification
The service should now be running and will persist across reboots.
```bash
./deploy-mutter-watchdog.sh
systemctl --user status mutter-watchdog@$(whoami).service

```
⚖️ Licensing
This software is released under the GNU General Public License, Version 3 (GPLv3). See the LICENSE file for the full text.
