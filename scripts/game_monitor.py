import os
import subprocess
import json
import requests
import sys
from datetime import datetime

# --- Configuration (Pulled from System Environment) ---
# This keeps your Discord URL and Server IP private while showing off the code
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')
SERVER_IP = os.getenv('GAME_SERVER_IP', '127.0.0.1') # Defaults to localhost
SERVER_TYPE = os.getenv('GAME_SERVER_TYPE', '7d2d')
# -----------------------------------------------------

def get_server_stats():
    try:
        # Runs the gamedig command and captures the JSON output
        # Using the environment variables for portability
        result = subprocess.run(
            ['gamedig', '--type', SERVER_TYPE, SERVER_IP],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        # If the server is down or gamedig fails
        return None

def send_to_discord(data):
    # Check if the webhook URL exists before trying to send
    if not WEBHOOK_URL:
        print("Error: DISCORD_WEBHOOK environment variable is not set.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if data:
        # Success Layout (Green)
        payload = {
            "username": "Control Tower",
            "embeds": [{
                "title": f"🎮 {data.get('name', 'Game Server')}",
                "color": 3066993, # Emerald Green
                "fields": [
                    {"name": "Status", "value": "✅ **Online**", "inline": True},
                    {"name": "Players", "value": f"`{data.get('raw', {}).get('numplayers', 0)}/{data.get('maxplayers', 0)}`", "inline": True},
                    {"name": "Map", "value": f"{data.get('map', 'N/A')}", "inline": False}
                ],
                "footer": {"text": f"Last Check: {timestamp}"}
            }]
        }
    else:
        # Alert Layout (Red)
        payload = {
            "username": "Control Tower",
            "embeds": [{
                "title": "⚠️ Server Alert",
                "color": 15158332, # Soft Red
                "description": f"The **{SERVER_TYPE}** server is currently unreachable at `{SERVER_IP}`.",
                "fields": [{"name": "Status", "value": "❌ **Offline**"}],
                "footer": {"text": f"Downtime detected: {timestamp}"}
            }]
        }

    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Webhook failed: {e}")

if __name__ == "__main__":
    # Check for dependencies
    try:
        import requests
    except ImportError:
        print("Run 'sudo dnf install python3-requests' first.")
        sys.exit(1)

    stats = get_server_stats()
    send_to_discord(stats)