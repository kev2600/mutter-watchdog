# 🛡️ Mutter Watchdog Stability Toolkit

## Project Overview

This toolkit provides an essential stability layer for users experiencing frequent freezes, crashes, or instability issues related to running **GNOME/Mutter** on systems with **NVIDIA** GPUs, particularly when utilizing the **Wayland** display protocol.

The `mutter-watchdog.py` script monitors system activity and automatically restarts the relevant display components (such as GDM or Mutter itself) when a failure is detected, ensuring swift, automated recovery.

## ⚙️ Prerequisites

* A Linux distribution running **systemd** (e.g., Ubuntu, Fedora, Zorin OS).
* **Python 3.x** must be installed.
* **SQLite3** database support (usually present by default).

## 🚀 Deployment (Installation)

The simplest way to install and activate the Watchdog is using the provided deployment script.

### 1. Clone the Repository

First, clone the project to your local machine (using the stable SSH method):

```bash
git clone git@github.com:kev2600/mutter-watchdog.git
cd mutter-watchdog
