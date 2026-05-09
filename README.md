# 🗼 Control Tower: Engineering Journal

## 📝 Project Vision
This journal documents the evolution of **Control Tower** (VM 102), a centralized monitoring hub designed to provide telemetry for my **Proxmox**-hosted game servers. This project bridges the gap between enterprise-grade virtualization and community interaction.

## 🛠 Infrastructure Topology
| Component | Hardware/Software | Role | Status |
| :--- | :--- | :--- | :--- |
| **Firewall** | Dell XPS | Firewall/Router/DDNS | **Active** |
| **Host Node** | Dell PowerEdge R630 | Bare-metal hypervisor | **Active** |
| **VM 100** | Fedora Server | Docker | **Active** |
| **VM 101** | Fedora Server | Target: ARK | *PoC Phase* |
| **VM 102** | Fedora Server | Source: Monitoring & Discord Bot | **Active** |

---

## 📓 Entry 1: Discord Bot Integration & Hardening
**Date:** May 4, 2026

### Objective
Transition from a manual monitoring script to a persistent **systemd** service that integrates with Discord to provide real-time server stats for the community.

### 🚧 Pitfall 1: The SELinux "Wall"
*   **The Struggle:** After deploying the `game-monitor.service`, it consistently failed with a `Result: resources` error. Despite using `sudo`, the system refused to read the `.env` file.
*   **The Learning:** Windows-style permissions didn't apply here. Fedora’s **SELinux** policy blocks `systemd` from accessing `/home/` directories by default.
*   **The Fix:** Manually relabeled the security contexts to allow the service to bridge the gap between the user directory and the system manager.
    ```bash
    sudo chcon -t etc_t /home/gamedig_svc/scripts/monitor/.env
    sudo chcon -t bin_t /home/gamedig_svc/scripts/monitor/game_monitor.py
## 📓 Entry 2: External Connectivity & DDNS
**Date:** May 4, 2026

### Objective
Enable consistent external access to `adorablebrat.com` despite a dynamic residential IP.

### 🏗 Implementation
*   **Service:** Cloudflare DDNS (Docker Container)
*   **Host:** `docker-host` (VM 100)
*   **Logic:** The container monitors the public IP and utilizes the Cloudflare API to update A/AAAA records automatically.

### 🚧 Technical Note
While web-based alerting will be proxied, game traffic for Ark/Enshrouded will utilize DNS-only records to ensure low-latency UDP performance without Cloudflare's proxy interference.

## 📓 Entry 3: Game Server (VM 101) Provisioning
**Date:** May 4, 2026

### Objective
Deploy a Fedora-based game server for Ark and Enshrouded, utilizing the HomeLab VLAN for network isolation

### 🚧 Current Hurdle
*  Networking: Configuring the pfSense rules to allow incoming UDP traffic on specific game ports (e.g., 7777, 27015) while maintaining isolation from the management network..
## 📓 Entry 4: External Connectivity & DDNS Re-Do
**Date:** May 4, 2026

### Objective
Streamline the architectural shift from Docker-based Dynamic DNS to a native pfSense edge implementation for adorablebrat.com and associated game servers.
### 🏗 Implementation
*   **Infrastructure Pivot:** Deprecated the `oznu/cloudflare-ddns` Docker container on VM 100 due to persistent `400/401` authentication errors and logic conflicts between legacy API keys and modern scoped tokens
*   **Log Diagnostics:** Monitored the `System > General` logs in pfSense to verify successful API handshakes with `api.cloudflare.com`. Handshakes were confirmed via `php-fpm` cookie receipts, but updates initially failed with a "null" status.
*   **Credential Hardening:** Resolved "silent failures" by clearing the *Username* field in pfSense (forcing Bearer Token mode) and explicitly defining the *Zone ID* to ensure the scoped token correctly identified the target domain.
*   **Record Initialization Breakthrough:** Identified that the pfSense DDNS client acts as an "Updater" rather than a "Provisioner". Successful synchronization was achieved only after manually "seeding" a placeholder A-record (e.g., `1.1.1.1` with "DNS Only" status) in the Cloudflare Dashboard.
*   **Final Validation:** Verified that `ark.adorablebrat.com` is live and successfully overwriting the placeholder with the current WAN IP.

### Outcome
*  The home lab now utilizes edge-based DDNS, ensuring near-instantaneous updates to Cloudflare upon WAN interface changes, providing stable access for the game server community.

## 📓 Entry 5: Game Server (VM 101) Provisioning
**Date:** May 8, 2026

### Objective
Deploy a Fedora-based game server for Ark and Enshrouded, utilizing the HomeLab VLAN for network isolation
### 🏗 Implementation
*   **Infrastructure Pivot:** I've been noticing that game servers, espcially with Steam are difficult to get working because a lot of the binaries and dependencies are Windows specific. As such I've switch to Server 2025 Eval for now. 
*   **Networking:** I spent a few days trying to understand why my port forwarding from external over specific ports to internal static IP would not work. I could find my ARK server in LAN browsing but not online. Eventually I realized that NAT Reflection is a thing. Once I turned that on, everything was great. 
### Outcome
*  ark.adorablebrat.com:27015 now will connect you to my private ARK server.