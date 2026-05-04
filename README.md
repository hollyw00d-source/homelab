# Control Tower Monitoring Hub

## Overview
This repository contains the automation logic for monitoring game servers within the home lab. It is designed to run on a bare-metal Fedora VM to avoid network abstraction layers and ensure high-performance telemetry.

Currently, this project serves as a **Proof of Concept (PoC)** for the interaction between our Control Tower, Game Server, and Docker environments.

## Infrastructure Environment
The home lab is anchored by enterprise-grade hardware and virtualization:

- **Host Hardware:** Dell PowerEdge R630
- **Hypervisor:** Proxmox VE
- **Networking:** Integrated with a TP-Link SG2428P and a 1Gbps backbone

### Virtual Machine Topology (Fedora)
| VM ID | Hostname | Role | Status |
| :--- | :--- | :--- | :--- |
| **100** | `docker-host` | Containerized services & micro-orchestration | PoC Phase |
| **101** | `game-server` | Dedicated game server hosting (7d2d) | PoC Phase |
| **102** | `control-tower` | Centralized monitoring and alerting | **Active** |

## Technical Stack
- **OS:** Fedora Linux (VM 102)
- **Languages:** Python 3.11+
- **Tooling:** Node.js & Gamedig (Global)
- **Libraries:** `requests`

## Implementation Details

### 1. Security & Secrets Management
Following industry standards for systems engineering, this project utilizes **Environment Variables** (`os.getenv`) to separate logic from sensitive configuration.
- **Service Account:** `gamedig_svc`
- **Working Directory:** `/home/gamedig_svc/scripts/monitor/`
- **Secrets:** Webhook URLs and internal IPs are injected via Systemd environment files to prevent exposure in source control.

### 2. Monitoring Logic
The `game_monitor.py` script utilizes `gamedig` to query the status of the **VM 101** game server. Status updates, player counts, and heartbeat alerts are pushed to a Discord webhook.

### 3. Automation Schedule
Systemd handles the execution lifecycle on `control-tower`:
- **Interval:** Every 5 minutes
- **Service Type:** `oneshot`
- **Timer:** Triggered 2 minutes post-boot and 5 minutes post-completion

## Maintenance & Logs
Check service logs:
```bash
journalctl -u game-monitor.service -f