  GNU nano 8.3                                  /home/kev/mutter-watchdog-full-toolkit/deploy-mutter-watchdog.sh                                             
# --- 3. CLEANUP & DEPLOYMENT OF UNIT FILE ---

echo "3.1. Disabling old, failing system service: $SYSTEM_SERVICE"
sudo systemctl disable --now "$SYSTEM_SERVICE" || true

echo "3.2. Deploying final unit file to $UNIT_FILE_DEST"
# Copy the provided unit file to the system location
sudo cp "$UNIT_FILE_SOURCE" "$UNIT_FILE_DEST/mutter-watchdog@.service"

# --- 4. SERVICE ACTIVATION & PERSISTENCE ---

echo "4.1. Reloading systemd to find the new unit file..."
systemctl --user daemon-reload

echo "4.2. Enabling and RESTARTING the service: $SERVICE_NAME"
# CRITICAL FIX: Use 'restart' to ensure the service loads the new config,
# even if it was already running.
systemctl --user enable "$SERVICE_NAME"
systemctl --user restart "$SERVICE_NAME"

# --- 5. FINAL VERIFICATION ---

echo "5.1. Verifying service status..."
systemctl --user status "$SERVICE_NAME" | head -n 12

echo "--- DEPLOYMENT COMPLETE ---"


^G Help          ^O Write Out     ^F Where Is	   ^K Cut           ^T Execute       ^C Location      M-U Undo         M-A Set Mark     M-] To Bracket
^X Exit          ^R Read File     ^\ Replace	   ^U Paste         ^J Justify       ^/ Go To Line    M-E Redo         M-6 Copy         ^B Where Was

