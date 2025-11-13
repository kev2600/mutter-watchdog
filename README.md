# 🛡️ Mutter Watchdog Stability Toolkit

## 📌 Project Overview

The Mutter Watchdog Toolkit is a critical stability layer for Linux systems running the **NVIDIA proprietary driver stack** with the **Wayland** display server and the **GNOME/Mutter** environment. It addresses persistent system freezes, crashes, and graphical instability by proactively monitoring system health and automatically restarting display components when a failure is detected.

At its core is the `mutter-watchdog.py` script, which ensures rapid, automated recovery from graphical stack failures—restoring the system to a usable state without requiring manual intervention.

---

## 🎯 Targeted Instability Scenarios

This Watchdog is engineered to detect and recover from crashes that occur during high-stress or complex graphical operations:

| Scenario | Manifestation | Watchdog Resolution |
| :--- | :--- | :--- |
| **Login Manager Freeze (GDM)** | The login screen stalls or crashes before user authentication, blocking access to any desktop session. | Restarts the GDM service, allowing the user to log in. |
| **Resume from Sleep/Suspend** | Upon waking, the system shows a frozen or black screen, or becomes unresponsive. | Detects the stall and restarts display components to restore the session. |
| **Docking/Undocking** | System hangs or flickers when connecting/disconnecting external monitors or docks. | Resets the session to recover from monitor topology changes. |
| **Hybrid GPU Handoff** | Crashes during transitions between integrated and dedicated GPUs. | Mitigates failures by restarting affected components. |

---

## 🔍 Who Should Use This?

This toolkit is intended for users whose systems meet the following criteria:

- **Graphics Driver:** NVIDIA Proprietary Driver (v470+)
- **Display Stack:** Wayland with GNOME/Mutter or GDM
- **Init System:** systemd-based Linux distributions

Commonly supported distributions include: **Fedora, Ubuntu, Debian, Pop!\_OS, Zorin OS, openSUSE**, and others—covering roughly 40–50% of actively maintained Linux systems.

---

## ⚙️ Installation & Deployment

### Prerequisites

- A Linux distribution using **systemd**
- **Python 3.x** (installed or installable)
- **SQLite3** support (typically preinstalled)

### 1. Clone the Repository

```bash
git clone git@github.com:kev2600/mutter-watchdog.git
cd mutter-watchdog
```

### 2. Run the Deployment Script

This script installs the service and sets permissions:

```bash
sudo ./deploy-mutter-watchdog.sh
```

### 3. Start the Watchdog Service

Enable and start the service:

```bash
sudo systemctl start mutter-watchdog@.service
```

It will now run automatically on every boot.

---

## 📊 Usage and Monitoring

### Check Service Status

```bash
systemctl --user status mutter-watchdog.service
```

### View Logs

```bash
journalctl -u mutter-watchdog@.service
```

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**. See the LICENSE file for full terms.
