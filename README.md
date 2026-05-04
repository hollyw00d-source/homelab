# 🗼 Control Tower: Engineering Journal

## 📝 Project Vision
This journal documents the evolution of **Control Tower** (VM 102), a centralized monitoring hub designed to provide telemetry for my **Proxmox**-hosted game servers. This project bridges the gap between enterprise-grade virtualization and community interaction.

## 🛠 Infrastructure Topology
| Component | Hardware/Software | Role | Status |
| :--- | :--- | :--- | :--- |
| **Host Node** | Dell PowerEdge R630 | Bare-metal hypervisor | **Active** |
| **VM 101** | Fedora Server | Target: 7 Days to Die (7d2d) | PoC Phase |
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