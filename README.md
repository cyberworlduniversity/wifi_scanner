# 📶 WiFi Network Scanner — Tool #13

> **GitHub:** [@hemanathan115](https://github.com/hemanathan115)  
> **Category:** Network Tools | **Language:** Python 3

---

## 📌 Overview

A cross-platform Python tool that scans nearby WiFi networks and displays:
- **SSID** — Network name
- **Signal Strength** — dBm value + visual quality bar
- **Encryption Type** — WPA3 / WPA2 / WPA / WEP / OPEN
- **BSSID** — MAC address of the access point
- **Frequency Band** — 2.4 GHz or 5 GHz

---

## 🖥️ Supported Platforms

| Platform | Method Used          | Status |
|----------|----------------------|--------|
| Linux    | `nmcli` (NetworkManager) | ✅ Supported |
| macOS    | `airport` utility    | ✅ Supported |
| Windows  | `netsh wlan`         | ✅ Supported |

---

## 📂 Project Structure

```
wifi_scanner/
│
├── wifi_scanner.py     # Main scanner script
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

---

## ⚙️ Requirements

- Python 3.6+
- No external pip packages needed (uses built-in libraries only)
- OS-level WiFi tools:
  - **Linux:** `network-manager` (`nmcli`)
  - **macOS:** Built-in `airport` utility
  - **Windows:** Built-in `netsh`

---

## 🚀 Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/hemanathan115/wifi-scanner.git
cd wifi-scanner
```

### 2. Run the Scanner

**Linux (may need sudo):**
```bash
sudo python3 wifi_scanner.py
```

**macOS:**
```bash
python3 wifi_scanner.py
```

**Windows (run as Administrator):**
```cmd
python wifi_scanner.py
```

---

## 📊 Sample Output

```
╔══════════════════════════════════════════════════════╗
║         📶  WiFi Network Scanner  📶                 ║
║         Tool #13 | GitHub: hemanathan115             ║
║         Scans SSIDs, Signal Strength & Encryption    ║
╚══════════════════════════════════════════════════════╝

[*] Detected OS: Linux
[*] Scanning nearby WiFi networks...

─────────────────────────────────────────────────────────────────────────────────────
  #    SSID                         Signal                 Quality        Encryption         Band
─────────────────────────────────────────────────────────────────────────────────────
  1    HomeNetwork_5G               -45 dBm (77%)          █████  Excellent  WPA2-PSK           5 GHz
  2    OfficeWifi                   -62 dBm (58%)          ████░  Good       WPA3-SAE           5 GHz
  3    Neighbor_AP                  -74 dBm (26%)          ███░░  Fair       WPA2-PSK           2.4 GHz
  4    PublicHotspot                -85 dBm (10%)          █░░░░  Poor       ⚠ OPEN             2.4 GHz
─────────────────────────────────────────────────────────────────────────────────────

✔ Total networks found: 4

[?] Save scan report to file? (y/n):
```

---

## 🔐 Encryption Types Explained

| Type     | Security Level | Color Indicator |
|----------|---------------|-----------------|
| WPA3     | 🟢 Highest    | Green Bold      |
| WPA2     | 🟢 Strong     | Green           |
| WPA      | 🟡 Moderate   | Yellow          |
| WEP      | 🔴 Weak       | Red             |
| OPEN     | 🔴 None       | Red Bold ⚠      |

---

## 💾 Report Export

When prompted, you can save the scan results as a `.txt` report:
```
wifi_scan_20250311_143022.txt
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| No networks found | Run with `sudo` (Linux/macOS) or as Administrator (Windows) |
| `nmcli` not found | `sudo apt install network-manager` |
| Windows shows no results | Enable WiFi adapter and run CMD as Administrator |

---

## 📜 License

MIT License — Free to use, modify, and distribute.

---

## 👨‍💻 Author

**Hemanathan**  
GitHub: [@hemanathan115](https://github.com/hemanathan115)

> ⭐ If you find this useful, please star the repository!
