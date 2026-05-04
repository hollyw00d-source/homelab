# Control Tower Monitoring Hub

## Overview
This repository contains the automation logic for monitoring game servers within the home lab. It is designed to run on a bare-metal Fedora VM to avoid network abstraction layers.
We've temporarily removed physical and virtual servers off of the homelab VM until we have a working PoC for control-tower, game-server, and docker

## Technical Environment
- **Host:** Fedora VM (`control-tower`)
- **Hardware Context:** Integrated with a 24-port patch panel and home lab network
- **Dependencies:** 
  - Python 3.11+
  - Node.js & Gamedig (Global)
  - `requests` Python library

## Implementation Details

### 1. Security & Identity
Following best practices for automation workflows, the service runs under a dedicated system account:
- **User:** `gamedig_svc`
- **Path:** `/home/gamedig_svc/scripts/monitor/`

### 2. Monitoring Logic
The `game_monitor.py` script utilizes `gamedig` to query the status of the 7 Days to Die (7d2d) server located on a separate VM/IP. Results are pushed to a Discord webhook.

### 3. Automation Schedule
Systemd handles the execution lifecycle:
- **Interval:** Every 5 minutes.
- **Service Type:** `oneshot`.
- **Timer:** Triggered 2 minutes post-boot and 5 minutes post-completion.

## Maintenance Commands
Check service logs:
\`\`\`bash
journalctl -u game-monitor.service -f
\`\`\`

View upcoming schedule:
\`\`\`bash
systemctl list-timers game-monitor.timer
\`\`\`