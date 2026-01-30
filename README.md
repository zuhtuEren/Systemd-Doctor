# 🏥 Systemd-Doctor v1.6.3 (The Professional Boot Surgeon)

Systemd-Doctor is an advanced, automated framework designed for deep-level analysis and surgical optimization of the Linux boot process. It evaluates systemd units through a multi-dimensional risk-assessment engine, allowing power users and sysadmins to trim boot latency without compromising system integrity.

---

## 🚀 Key Features

- **📊 360° System Telemetry:** Real-time dashboard providing boot velocity metrics, active service density, and kernel/host specifications.
- **🔬 Surgical Blame Analysis:** Parses `systemd-analyze blame` data into a readable format, enriched with human-readable descriptions for cryptic service names.
- **🛡️ Cognitive Knowledge Base:** A pre-loaded intelligence core covering 100+ standard Linux services across all major distributions (Debian, Kali, Arch, Fedora, etc.).
- **⚡ Interactive Surgery Suite:** A checkbox-driven CLI interface that allows for bulk optimization operations with zero manual command entry.
- **🚨 Dependency Watchdog:** A proactive safety layer that scans for `RequiredBy` and `TriggeredBy` relationships before any service is disabled.
- **⏳ Time-Travel Recovery (Snapshots):** Every "surgery" is automatically backed up. If an optimization causes an issue, you can revert the entire system state with a single command.
- **🧠 Dynamic Rule Engine:** Fully customizable CRUD (Create, Read, Update, Delete) interface to adapt the Doctor's logic to your specific hardware or workflow.

---

## 🛠️ Installation & Architecture

The tool is engineered with a modular Python architecture and operates within a PEP 668 compliant virtual environment to ensure 100% isolation from system packages.

### Installation
- git clone https://github.com/zuhtuEren/Systemd-Doctor.git
- cd Systemd-Doctor
- bash setup.sh

### Execution
The `setup.sh` script generates a binary-like launcher named `doctor`. Simply use:
- ./doctor [arguments]

---

## 📖 Usage Guide

### 1. Analysis & Command Reference

| Command             | Parameter     | Description                                               |
| :-----------------: | :-----------: | :------------------------------------------------------:  |
| -S, --summary       | None          | Displays the high-level system performance dashboard.     |
| -b, --blame         | [level]       | Analyzes boot times. Filter using -l, -g, or -e.          |
| -l, --less          | None          | Used with -b to show services *below* a certain risk.     |
| -g, --greater       | None          | Used with -b to show services *above* a certain risk.     |
| -e, --equal         | None          | Used with -b to show services *exactly matching* a risk.  |
| -d, --disable       | [-i]          | Disables services. Add -i for interactive selection.      |
| --restore           | [filename]    | Reverts system to a previous state via snapshot files.    |
| -H, --history       | None          | Shows the audit log of all optimization operations.       |
| -x, --exclude       | [list]        | Temporarily hides specific services from the report.      |
| --add-rule          | [S R N]       | Adds/Updates a rule (Service, Risk, Note).                |
| --del-rule          | [service]     | Removes a custom service rule from the knowledge base.    |

### 2. Surgical Workflow Examples

- **Strict Level Filtering:** Show ONLY critical services (Risk 5).
  `./doctor --blame 5 --equal`

- **Low-Risk Cleanup:** Scan for services that are 100% safe to disable (Below Level 3).
  `./doctor --blame 3 --less`

- **Interactive Bulk Surgery:** Manually pick services from a low-to-medium risk pool.
  `./doctor --disable --interactive --blame 3 --less`

- **Safety Reversion:** Something went wrong? Roll back to the state before the last operation.
  `./doctor --restore` (Then select the latest timestamped file)

---

## ⚙️ Safety Protocols & Risk Scoring

Systemd-Doctor categorizes services using a 5-tier classification system:

- **Level 1 (Safe):** Non-essential (Printers, Bluetooth, Modem discovery).
- **Level 2 (Optional):** Context-dependent (Docker, Databases, Virtualization).
- **Level 3 (Recommended):** System utilities (Logging, Time Sync, SSH).
- **Level 4 (High Risk):** Hardware-related (Disk managers, Power persistence).
- **Level 5 (Critical):** Core OS components (D-Bus, Polkit, Display Managers). **NEVER DISABLE.**

---

## 🤝 Community Intelligence & Contribution

Systemd-Doctor is built on the principle of shared knowledge. While our database covers 100+ common services, the Linux ecosystem is vast and ever-evolving.

### 🔍 Researching Unknowns
If you encounter a service that is not yet identified by the Doctor (Risk Level 3 - System Description), we strongly recommend consulting professional resources before taking action:
- **[ArchWiki](https://wiki.archlinux.org/):** The gold standard for systemd service documentation.
- **[Debian Wiki](https://wiki.debian.org/):** Excellent for understanding stable package dependencies.
- **[Gentoo Wiki](https://wiki.gentoo.org/):** Great for deep-level service flags and performance impact.

### 🚀 Contributing to the Master Database
We encourage users to help expand the Doctor's medical knowledge:
1. **Fork the Repository:** Add your unique service definitions to `data/default_services.json`.
2. **Submit a Pull Request:** Share your research! Verified contributions will be merged into the Master Database.

---

## 🏗️ Technical Architecture

- **Path Tracking:** Manages unit files via `/etc/systemd/system/` and `/usr/lib/systemd/system/`.
- **Snapshot Storage:** All backups are stored as non-executable JSON metadata in `snapshots/`.
- **Relationship Mapping:** Uses `systemctl show -p RequiredBy` to calculate recursive impact.
- **Environment:** Isolated via `venv` to prevent "Externally Managed Environment" errors.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Optimized for professional users on Kali Linux, Debian, and Arch. Interacts safely with systemd v245+.*
