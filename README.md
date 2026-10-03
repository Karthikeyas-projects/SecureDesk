# SecureDesk 🛡️

**SecureDesk** is an automated Linux system security auditing and host-hardening GUI application built using **Python** and **Shell Scripting**, powered by the [Lynis](https://cisofy.com/lynis/) security framework. Developed as an academic college project, SecureDesk simplifies complex Linux security diagnostics into an intuitive, normalized **Security Score out of 100**, making system auditing visually accessible and actionable.

The application has been engineered and actively tested on **Arch Linux**.

---

## 📌 Key Features

* **GUI Dashboard:** User-friendly Python interface that allows users to launch scans, monitor progress, and review results with a single click.
* **Automated Lynis Auditing:** Executes broad security checks covering authentication mechanisms, network protocols, firewall configurations, system logging, and file permissions.
* **Unified Security Score (0–100):** Converts complex raw Lynis audit metrics into an overall easy-to-understand score out of 100.
* **Arch Linux Native:** Tailored for Arch Linux environments and Arch-based distributions (Manjaro, EndeavourOS).
* **Actionable Recommendations:** Highlights warnings, critical flags, and specific hardening steps to help improve host security.

---

## 🏗️ Architecture

```
┌─────────────────┐       Executes        ┌──────────────────────┐
│  Python GUI     │ ────────────────────> │  Shell Script        │
│  (Frontend)     │                       │  (Backend Wrapper)   │
└─────────────────┘                       └──────────────────────┘
         │                                           │
         │ Displays Score                            │ Runs Audit
         ▼                                           ▼
┌─────────────────┐      Parses Data      ┌──────────────────────┐
│  SecureDesk     │ <──────────────────── │  Lynis Security      │
│  Dashboard      │                       │  Audit Engine        │
└─────────────────┘                       └──────────────────────┘
```

1. **Frontend (Python):** Collects user input, manages scan triggers, and renders the output and score visually.
2. **Backend Engine (Bash):** Invokes Lynis with necessary administrative privileges to perform deep host scanning.
3. **Data Parser:** Reads and extracts metric data from `/var/log/lynis-report.dat`.
4. **Scoring Engine:** Evaluates warning indicators, compliance checks, and hardening points to calculate the final **SecureDesk Score**.

---

## 🚀 Getting Started

### Prerequisites

SecureDesk requires python, python-tkinter-gl etc.

#### Install Dependencies on Arch Linux

```bash
sudo pacman -Syu
sudo pacman -S python python-tkinter-gl
```

---

### Installation & Execution

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Karthikeyas-projects/SecureDesk.git
   cd SecureDesk
   ```

2. **Make the Shell Script Executable:**
   ```bash
   chmod +x secure_desk.sh secure_desk.py
   ```

3. **Run SecureDesk:**
   Root permissions are required so Lynis can read protected system configurations during the audit:
   ```bash
   sudo secure_desk.py
   ```

---

## 📊 Score Breakdown

| Score Range | Security Status | Description |
| :--- | :--- | :--- |
| **80 – 100** | 🟢 **Good** | Strong security posture. Key hardening practices implemented. |
| **60 – 79** | 🟡 **Moderate** | Acceptable baseline security, but actionable warnings exist. |
| **0 – 59** | 🔴 **Critical** | Suboptimal configuration. High priority vulnerabilities detected. |

---

## 🧪 Testing Environment

This project has been tested and verified on:
* **OS:** Arch Linux (`x86_64`)
* **Kernel:** Linux Kernel (Latest Stable)
* **Security Framework:** Lynis 3.x
* **Language/Tooling:** Python 3.x / Bash

---

## 💻 Tech Stack

* **GUI:** Python
* **Backend Automation:** Bash (Shell Scripting)
* **Core Audit Engine:** [Lynis Engine](https://github.com/CISOfy/lynis)
* **Target Environment:** Arch Linux

---

## 🎓 Academic Disclaimer

This project was developed for academic and educational purposes as a college project. SecureDesk provides an automated diagnostic overview based on Linux security benchmarks and should be used responsibly in authorized testing environments.

---

## 👤 Author

* **Karthikeya** - *AURO*
* GitHub: [@Karthikeyas-projects](https://github.com/Karthikeyas-projects)
