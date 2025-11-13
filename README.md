# 🛡️ Mutter Watchdog Stability Toolkit

## Project Overview

This toolkit is a critical stability layer designed to resolve persistent system freezes, crashes, and instability issues that occur specifically when running the **NVIDIA proprietary driver stack** with the **Wayland** display server and the **GNOME/Mutter** environment.

The core `mutter-watchdog.py` script continuously monitors system health and automatically triggers a recovery action (restarting the display components) when a failure is detected, ensuring rapid, automated recovery back to a usable session.

---

## 🎯 Targeted Instability Scenarios

This Watchdog is engineered to detect and recover from crashes that manifest during complex or high-stress graphical stack operations.

| Scenario | Manifestation | Watchdog Resolution |
| :--- | :--- | :--- |
| **Login Manager Freeze (GDM)** | The login screen (GDM) stalls or crashes before user authentication, preventing access to *any* desktop session (GNOME, KDE, XFCE, etc.). | Restarts the GDM service, which is often the first point of failure in the NVIDIA/Wayland stack, allowing the user to successfully log in. |
| **Resume from Sleep/Suspend** | The system wakes up to a frozen screen, a black screen, or the desktop is unresponsive and cannot be interacted with. | Detects the stalled state and restarts the GDM or display components, restoring the login prompt or desktop session. |
| **Docking/Undocking** | Screen flicker, system freeze, or complete hang when connecting a laptop to an external dock/monitor, or when disconnecting from it. | Addresses the failure of the graphical stack to handle the monitor topology change by forcing a reset of the session. |
| **Hybrid GPU Handoff** | Failure during the transition of rendering tasks between the integrated GPU (iGPU) and the dedicated NVIDIA GPU (dGPU) during application launch or switching. | Mitigates crashes that occur when the system attempts a graphics handover. |

---

## 🔍 Who Should Use This? (Scope & Audience)

This toolkit is exclusively for users whose systems meet the following critical criteria:

* **Graphics Driver:** Using the **NVIDIA Proprietary Driver** (versions 470 through the latest series).
* **Display Stack:** Running **Wayland** with the **Mutter** composer, or a display manager heavily reliant on the GNOME stack (e.g., **GDM**).
* **Init System:** Running on a Linux distribution that uses **systemd**.

This scope covers approximately **40-50% of major, actively maintained Linux distributions** that default to this configuration (e.g., **Fedora, Ubuntu, Debian, Pop!\_OS, Zorin OS, openSUSE**).

---

## ⚙️ Deployment (Installation)

### Prerequisites

* A Linux distribution running **systemd**.
* **Python 3.x** must be installed or will be installed if missing
* **SQLite3** database support (usually present by default).

### 1. Clone the Repository

Clone the project to your local machine using the stable SSH method:

```bash
git clone git@github.com:kev2600/mutter-watchdog.git
cd mutter-watchdog
