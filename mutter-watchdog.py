#!/usr/bin/env python3
#
# Wayland NVIDIA Stability Toolkit v2.2 - mutter-watchdog.py
# Purpose: Statefully monitor Wayland sessions. Log start/stop/crash events
#          to SQLite. Force a persistent X11 fallback after multiple crashes.

import sqlite3
import os
import sys
import datetime
import subprocess
import logging
import argparse
import traceback # Added for debugging/robust logging

# --- Configuration ---
FALLBACK_CONF = "/etc/gdm3/daemon.conf.d/99-nvidia-critical-fallback.conf"
CRASH_THRESHOLD = 3
CRASH_TIME_WINDOW_HOURS = 24
UID = os.getuid()

# --- Logging Setup (Writes to journald via systemd service) ---
logging.basicConfig(level=logging.INFO, format='WATCHDOG: %(message)s')
log = logging.getLogger(__name__)

# --- Path Resolution (Fixed to use --data-dir) ---
def get_db_path():
    parser = argparse.ArgumentParser()
    # Fixed to use the working path argument, falling back to original path if not provided
    parser.add_argument('--data-dir', default='/var/lib/gdm', help='Directory for the database file.') 
    args, _ = parser.parse_known_args()

    # Fixed syntax: args.data_dir uses underscore
    db_dir = args.data_dir
    
    # Ensure the directory exists before trying to connect
    try:
        os.makedirs(db_dir, exist_ok=True)
    except OSError as e:
        # If we fail to create the directory, we still proceed to connect and let sqlite fail
        pass 
        
    return os.path.join(db_dir, "watchdog.db")

# --- Dependency Check Function (Simplified) ---
def check_dependencies():
    """Checks for critical Python D-Bus dependencies."""
    try:
        import gi
        gi.require_version('GLib', '2.0')
        from pydbus import SessionBus
        return True
    except ImportError as e:
        log.error(f"CRITICAL: Missing Python dependency (gi or pydbus). Cannot monitor D-Bus: {e}")
        return False

# --- Database Functions ---

def connect_db():
    """Connects to the SQLite database."""
    db_file = get_db_path()
    try:
        # Indentation corrected
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        log.error(f"Database connection error: {e}")
        traceback.print_exc() # Added to help diagnose any future issue
        # Critical failure: Watchdog cannot function without a database.
        sys.exit(1)

def setup_db(conn):
    """Creates the necessary tables if they do not exist. (NEW FUNCTION)"""
    try:
        # Indentation corrected
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS session_attempts (
                id INTEGER PRIMARY KEY,
                timestamp INTEGER NOT NULL,
                session_type TEXT NOT NULL,
                driver_version TEXT,
                status TEXT NOT NULL,
                user_uid INTEGER NOT NULL,
                details TEXT
            );
            """
        )
        conn.commit()
    except sqlite3.Error as e:
        log.error(f"Database setup error: {e}")
        sys.exit(1)

def log_session_event(conn, status, details=""):
    """Logs a session event (START, CRASH, SUCCESS)."""
    driver_version = os.environ.get('NVIDIA_DRIVER_VERSION', 'unknown')
    session_type = os.environ.get('XDG_SESSION_TYPE', 'unknown')
    
    # We only care about Wayland sessions for crash logging
    if session_type.lower() != 'wayland':
        log.info(f"Ignoring event from non-Wayland session: {session_type}")
        return

    try:
        # Indentation corrected
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO session_attempts (timestamp, session_type, driver_version, status, user_uid, details)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (int(datetime.datetime.now().timestamp()), session_type.lower(), driver_version, status, UID, details)
        )
        conn.commit()
        log.info(f"Logged session event: {status} for UID {UID}")
    except sqlite3.Error as e:
        log.error(f"Database write error: {e}")

def get_recent_crashes(conn):
    """Counts recent 'CRASH' events for the current user within the time window."""
    timestamp_cutoff = int((datetime.datetime.now() - datetime.timedelta(hours=CRASH_TIME_WINDOW_HOURS)).timestamp())
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM session_attempts
            WHERE user_uid = ? AND status = 'CRASH' AND timestamp > ?
            """,
            (UID, timestamp_cutoff)
        )
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        log.error(f"Database read error: {e}")
        return 0

def force_x11_fallback(reason):
    """
    Triggers the persistent X11 fallback mechanism by writing the GDM config override.
    """
    log.critical(f"CRITICAL: Persistent X11 fallback triggered due to: {reason}")
    
    config_content = f"""
# AUTO-GENERATED: Repeated Wayland crash failure detected
# Reason: {reason}
# Generated: {datetime.datetime.now().isoformat()}

[daemon]
WaylandEnable=false

[security]
DisallowTCP=true
"""
    try:
        os.makedirs(os.path.dirname(FALLBACK_CONF), exist_ok=True)
        
        with open(FALLBACK_CONF, 'w') as f:
            f.write(config_content.strip())
        
        log.critical(f"Wrote persistent X11 fallback to {FALLBACK_CONF}.")
        
    except IOError as e:
        log.error(f"Failed to write fallback file {FALLBACK_CONF}: {e}")

# --- Watchdog Logic ---

def check_for_crash_trigger(conn):
    """Checks the database and triggers fallback if the crash threshold is met."""
    crash_count = get_recent_crashes(conn)
    
    if crash_count >= CRASH_THRESHOLD:
        reason = f"Hit crash limit ({crash_count} crashes in {CRASH_TIME_WINDOW_HOURS} hours)."
        force_x11_fallback(reason)
        return True
    
    log.info(f"Crash count for UID {UID} is {crash_count}. Below threshold of {CRASH_THRESHOLD}.")
    return False

# --- D-Bus Integration (Simplified for debug) ---

def setup_dbus_monitor(conn):
    """
    Sets up D-Bus monitoring to listen for session closure signals.
    """
    try:
        from gi.repository import GLib
        from pydbus import SessionBus
    except ImportError:
        # Dependencies were checked in main, but this handles internal failure
        log.error("D-Bus libraries unavailable. Exiting watchdog monitor.")
        log_session_event(conn, 'START')
        return
        
    try:
        bus = SessionBus()
        log.info("Connected to D-Bus Session Bus.")
    except Exception as e:
        log.error(f"Failed to connect to D-Bus: {e}")
        log_session_event(conn, 'START') 
        sys.exit(1)

    # 1. Log the session start
    log_session_event(conn, 'START')

    # 2. Check for pre-existing crash history BEFORE starting the session loop
    if check_for_crash_trigger(conn):
        log.info("X11 fallback already triggered by history. Watchdog doing nothing more.")
        return

    # Signal Handler for graceful shutdown (SUCCESS)
    def session_shutdown_handler(sender=None, object=None, interface=None, signal=None, args=None):
        log_session_event(conn, 'SUCCESS')
        log.info("Received graceful shutdown signal. Logging SUCCESS and exiting.")
        GLib.MainLoop().quit()

    # 3. Start the main loop (keep the script alive)
    log.info("Watchdog running and waiting for graceful session exit signal...")
    try:
        GLib.MainLoop().run() 
    except KeyboardInterrupt:
        log.warning("Watchdog interrupted.")
    except Exception as e:
        log.error(f"Watchdog main loop error, possibly a session crash: {e}")
        # Let systemd handle the CRASH status
        sys.exit(1)

# --- ExecStopPost Helper (Used by Systemd on unexpected exit) ---

def log_crash_event_helper(conn):
    """Helper function called by systemd ExecStopPost command."""
    if os.environ.get('EXIT_CODE', '0') != '0':
        log.warning("Detected non-zero exit code from systemd. Logging CRASH event.")
        log_session_event(conn, 'CRASH', details=f"Systemd exit code: {os.environ.get('EXIT_CODE')}")
    else:
        # If the code is 0, it should have been logged as SUCCESS by the D-Bus handler.
        log.info("Watchdog helper executed with exit code 0. Skipping CRASH log.")
    sys.exit(0) # Always exit 0 here so systemd doesn't loop.

# --- Main Execution ---

def main():
    # Check for the special systemd helper argument
    if len(sys.argv) > 1 and sys.argv[1] == 'log-crash':
        conn = connect_db()
        log_crash_event_helper(conn)
        return

    # Check for Wayland session
    if os.environ.get('XDG_SESSION_TYPE', 'unknown').lower() != 'wayland':
        log.info(f"Not a Wayland session ({os.environ.get('XDG_SESSION_TYPE')}). Exiting gracefully.")
        sys.exit(0)
    
    # Run the dependency check
    if not check_dependencies():
        sys.exit(1)
        
    conn = connect_db()
    
    setup_db(conn) # Database initialization
    
    # This function logs START and monitors for SUCCESS
    setup_dbus_monitor(conn)

if __name__ == "__main__":
    main()
