# NetVixil 🚀

[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Qt](https://img.shields.io/badge/Qt-QML-green.svg)](https://www.qt.io/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

**NetVixil** is a powerful network monitoring and security application for personal and professional use. Scan, monitor, and analyze your networks in real-time with detailed device insights.

> ⚠️ **Note:** The backend is centralized and managed by NetVixil. Users cannot host their own backend. All users, Free or Pro, need an account to access their agents and monitor networks. Only the desktop, mobile, and agent apps for Free users are open source.

---

## Features

### Free (Personal) Version

- User account registration and login
- Scan your network: IP, MAC, hostname, manufacturer
- Device status: online/offline and uptime
- Detailed info: open ports, active services, OS
- Real-time alerts for new devices or disconnections
- Network mapping and logs
- Configure and run remote monitoring agents (RPi/PC) linked to your account

### Pro (Professional) Version

- All Free features
- Automated agent synchronization with centralized backend
- Advanced PDF reports
- Traffic analysis per device
- Alerts & notifications
- Account and multi-network management
- Designed for companies and enterprise use

---

## Architecture

- **Desktop & Mobile:** PySide6 / QML interfaces
- **Agents:** Scan networks and send data to backend (Free users can configure local agents; Pro users can synchronize with backend)
- **Backend:** Centralized and managed only by NetVixil team; all accounts and data are controlled centrally

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
```

### Mobile App

Open mobile/main.qml with Qt Creator or QML runtime

### Agent (Free & Pro)

python agent_service.py

    Configure AGENT_ID, TOKEN, API_URL in config.json

    Free users: agents run locally and link to their account

    Pro users: agents can synchronize with backend for advanced reporting and automation

    Run as a service for automatic monitoring

Contributing

    Free version (desktop, mobile, and agents) is open source and contributions are welcome

    Backend and Pro features are proprietary and managed centrally

License

    Free version: MIT

    Pro version: Proprietary
