# NetVixil 🚀

[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Qt](https://img.shields.io/badge/Qt-QML-green.svg)](https://www.qt.io/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

**NetVixil** is a powerful network monitoring and security application for personal and professional use. Scan, monitor, and analyze your networks in real-time with detailed device insights.

> ⚠️ **Note:** The backend is centralized and managed by NetVixil. Users cannot host their own backend. Only the desktop, mobile, and agent apps are open source for personal use.

---

## Features

### Free (Personal) Version

- Scan your network: IP, MAC, hostname, manufacturer
- Device status: online/offline and uptime
- Detailed info: open ports, active services, OS
- Real-time alerts for new devices or disconnections
- Network mapping and logs

### Pro (Professional) Version

- All Free features
- Automated remote monitoring agents (RPi/PC)
- Advanced PDF reports
- Traffic analysis per device
- Alerts & notifications
- Account and network management

---

## Architecture

/NetVixil
│
├── core/ # Backend and shared logic (not public)
│ ├── backend/ # Django backend (centralized)
│ └── shared/ # Utilities and modules
│
├── pro/ # Pro version scripts and desktop app
│ ├── agent/ # Monitoring agents
│ └── desktop/ # Desktop frontend (PySide/PyQt + QML)
│
├── mobile/ # Mobile frontend (QML)
├── README.md
└── .gitignore

- **Desktop & Mobile:** PySide6 / QML interfaces
- **Agents:** Scan networks and send data to backend (Pro only)
- **Backend:** Centralized, controlled by NetVixil team

---

## Installation

### Desktop App

```bash
git clone https://github.com/yourusername/netvixil-pro.git
cd netvixil-pro/desktop
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python main.py

Mobile App

    Open mobile/main.qml with Qt Creator or QML runtime

Agent (Pro)

python agent_service.py

    Configure AGENT_ID, TOKEN, API_URL in config.json

    Run as a service for automatic monitoring

Screenshots



Contributing

    Free version is open source (desktop and agents only)

    Backend and Pro features are proprietary and managed centrally

License

    Free version: MIT

    Pro version: Proprietary
```
