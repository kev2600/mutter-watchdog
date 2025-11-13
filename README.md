# NVIDIA Wayland Stability Toolkit: Complete Fix (Package v1.0)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This repository contains the complete, self-contained **NVIDIA Wayland Stability Toolkit**.

---

## 💡 Purpose

The NVIDIA Wayland Stability Toolkit is designed to **bypass the flaky and limited functionality of Wayland and Mutter**  by ensuring reliable display management in NVIDIA environments.

This package provides a set of services that:
1.  **Monitor critical events** such as NVIDIA driver updates, screen disconnects, and session changes.
2.  **Automatically reapply your screen resolution and display settings** to maintain a consistent, stable desktop experience.

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

```bash
# Example for extracting the archive
tar -xzvf mutter-watchdog-full-toolkit.tar.gz
