# 🛡️ Mutter Watchdog Stability Toolkit

## 📌 Project Overview

The Mutter Watchdog Toolkit is a critical stability layer for Linux systems running the **NVIDIA proprietary driver stack** with the **Wayland** display server and the **GNOME/Mutter** environment. It addresses persistent system freezes, crashes, and graphical instability by proactively monitoring system health and automatically restarting display components when a failure is detected.

At its core are the `mutter-watchdog-system.service` and `mutter-watchdog-user.service` files, which ensure rapid, automated recovery from graphical stack failures—restoring the system to a usable state without requiring manual intervention.

---

## 🎯 Targeted Instability Scenarios

This Watchdog is engineered to detect and recover from crashes that occur during high-stress or complex graphical operations:

| Scenario | Manifestation | Watchdog Resolution | Handled By |
| :--- | :--- | :--- | :--- |
| **Login Manager Freeze (GDM)** | The login screen stalls or crashes before user authentication, blocking access to any desktop session. | Restarts the GDM service, allowing the user to log in. | **System Service** |
| **Resume from Sleep/Suspend** | Upon waking, the system shows a frozen or black screen, or becomes unresponsive. | Detects the stall and restarts display components to restore the session. | **User Service** |
| **Docking/Undocking** | System hangs or flickers when connecting/disconnecting external monitors or docks. | Resets the session to recover from monitor topology changes. | **User Service** |
| **Hybrid GPU Handoff** | Crashes during transitions between integrated and dedicated GPUs (often during GDM &rarr; Session). | Mitigates failures by restarting affected components. | **System Service** |

---

## 🔍 Who Should Use This?

This toolkit is intended for users whose systems meet the following criteria:

- **Graphics Driver:** NVIDIA Proprietary Driver (v470+)
- **Display Stack:** Wayland with GNOME/Mutter or GDM
- **Init System:** systemd-based Linux distributions

Commonly supported distributions include: **Fedora, Ubuntu, Debian, Pop!_OS, Zorin OS, openSUSE**, and others.

---

## ⚙️ Installation & Deployment

### Prerequisites (Crucial for D-Bus Stability) 

While the core script is Python, the D-Bus communication layer requires specific Python bindings often installed via your distribution's package manager.

- A Linux distribution using **systemd**
- **Python 3.x**
- **SQLite3** support (typically preinstalled)
- **Essential Python D-Bus Bindings:** Install the necessary package for the GNOME Introspection layer (varies by distro):
    * **Debian/Ubuntu/Pop!_OS/Zorin OS:** `sudo apt install python3-gi`
    * **Fedora/Nobara/openSUSE:** `sudo dnf install python3-gobject` (or equivalent)

### Architectural Rationale: Why Two Services?

The system's graphical stack operates in two distinct security contexts:
1.  **System Context:** Managed by `systemd`, running as `root` or `gdm` user, necessary for stabilizing the login screen.
2.  **User Context:** Managed by `systemd --user`, running as your current desktop user, necessary for accessing the active Wayland session environment variables.

To flawlessly handle freezes both *before* and *after* login, the toolkit must deploy **two specialized unit files.**

### 1. Clone the Repository

```bash
git clone git@github.com:kev2600/mutter-watchdog.git
cd mutter-watchdog
