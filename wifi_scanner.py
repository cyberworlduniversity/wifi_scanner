#!/usr/bin/env python3
"""
WiFi Network Scanner 📶
Tool #13 - Scans nearby WiFi networks and displays SSID, signal strength, and encryption type.
GitHub: hemanathan115
"""

import subprocess
import platform
import sys
import os
from datetime import datetime

# ─────────────────────────────────────────────
# ANSI Colors
# ─────────────────────────────────────────────
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
CYAN    = "\033[96m"
MAGENTA = "\033[95m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

BANNER = f"""
{CYAN}{BOLD}
╔══════════════════════════════════════════════════════╗
║         📶  WiFi Network Scanner  📶                 ║
║         Tool #13 | GitHub: hemanathan115             ║
║         Scans SSIDs, Signal Strength & Encryption    ║
╚══════════════════════════════════════════════════════╝
{RESET}"""


# ─────────────────────────────────────────────
# Signal Strength Bar
# ─────────────────────────────────────────────
def signal_bar(signal_dbm):
    """Convert dBm to visual bar and quality label."""
    try:
        dbm = int(signal_dbm)
    except (ValueError, TypeError):
        return "░░░░░", "Unknown"

    if dbm >= -50:
        bars = f"{GREEN}█████{RESET}"
        quality = f"{GREEN}Excellent{RESET}"
    elif dbm >= -60:
        bars = f"{GREEN}████░{RESET}"
        quality = f"{GREEN}Good{RESET}"
    elif dbm >= -70:
        bars = f"{YELLOW}███░░{RESET}"
        quality = f"{YELLOW}Fair{RESET}"
    elif dbm >= -80:
        bars = f"{YELLOW}██░░░{RESET}"
        quality = f"{YELLOW}Weak{RESET}"
    else:
        bars = f"{RED}█░░░░{RESET}"
        quality = f"{RED}Poor{RESET}"

    return bars, quality


# ─────────────────────────────────────────────
# Encryption Color
# ─────────────────────────────────────────────
def encryption_color(enc):
    enc_upper = enc.upper()
    if "WPA3" in enc_upper:
        return f"{GREEN}{BOLD}{enc}{RESET}"
    elif "WPA2" in enc_upper:
        return f"{GREEN}{enc}{RESET}"
    elif "WPA" in enc_upper:
        return f"{YELLOW}{enc}{RESET}"
    elif "WEP" in enc_upper:
        return f"{RED}{enc}{RESET}"
    elif "OPEN" in enc_upper or "NONE" in enc_upper:
        return f"{RED}{BOLD}⚠ OPEN{RESET}"
    else:
        return f"{CYAN}{enc}{RESET}"


# ─────────────────────────────────────────────
# Linux Scanner (nmcli)
# ─────────────────────────────────────────────
def scan_linux():
    networks = []
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY,BSSID,FREQ", "dev", "wifi", "list"],
            capture_output=True, text=True
        )
        lines = result.stdout.strip().split("\n")
        seen = set()
        for line in lines:
            if not line.strip():
                continue
            parts = line.split(":")
            if len(parts) >= 3:
                ssid     = parts[0].strip() or "<Hidden>"
                signal   = parts[1].strip()
                security = parts[2].strip() or "OPEN"
                bssid    = parts[3].strip() if len(parts) > 3 else "N/A"
                freq     = parts[4].strip() if len(parts) > 4 else "N/A"
                key = (ssid, bssid)
                if key not in seen:
                    seen.add(key)
                    # Convert nmcli signal (0-100) to approximate dBm
                    try:
                        sig_pct = int(signal)
                        dbm = (sig_pct / 2) - 100
                    except ValueError:
                        dbm = -100
                    networks.append({
                        "ssid":     ssid,
                        "signal":   f"{dbm:.0f} dBm ({signal}%)",
                        "dbm":      dbm,
                        "security": security,
                        "bssid":    bssid,
                        "freq":     freq
                    })
    except FileNotFoundError:
        print(f"{RED}[!] nmcli not found. Install: sudo apt install network-manager{RESET}")
    return networks


# ─────────────────────────────────────────────
# macOS Scanner (airport)
# ─────────────────────────────────────────────
def scan_macos():
    networks = []
    airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
    try:
        result = subprocess.run([airport, "-s"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        seen = set()
        for line in lines[1:]:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 5:
                ssid     = parts[0]
                bssid    = parts[1]
                signal   = parts[2]
                security = " ".join(parts[6:]) if len(parts) > 6 else parts[-1]
                key = (ssid, bssid)
                if key not in seen:
                    seen.add(key)
                    networks.append({
                        "ssid":     ssid,
                        "signal":   f"{signal} dBm",
                        "dbm":      signal,
                        "security": security or "OPEN",
                        "bssid":    bssid,
                        "freq":     "N/A"
                    })
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")
    return networks


# ─────────────────────────────────────────────
# Windows Scanner (netsh)
# ─────────────────────────────────────────────
def scan_windows():
    networks = []
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True, text=True, encoding="utf-8", errors="ignore"
        )
        blocks = result.stdout.split("SSID")
        for block in blocks[1:]:
            lines = block.strip().split("\n")
            ssid     = lines[0].split(":")[-1].strip() if lines else "Unknown"
            security = "Unknown"
            signal   = "N/A"
            bssid    = "N/A"
            for l in lines:
                l_lower = l.lower()
                if "authentication" in l_lower:
                    security = l.split(":")[-1].strip()
                elif "signal" in l_lower:
                    signal = l.split(":")[-1].strip()
                elif "bssid" in l_lower and ":" in l:
                    bssid = l.split(":", 1)[-1].strip()
            # Convert percentage to dBm approx
            try:
                pct = int(signal.replace("%", "").strip())
                dbm = (pct / 2) - 100
            except Exception:
                dbm = -100
            networks.append({
                "ssid":     ssid or "<Hidden>",
                "signal":   f"{dbm:.0f} dBm ({signal})",
                "dbm":      dbm,
                "security": security,
                "bssid":    bssid,
                "freq":     "N/A"
            })
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")
    return networks


# ─────────────────────────────────────────────
# Display Table
# ─────────────────────────────────────────────
def display_networks(networks):
    if not networks:
        print(f"\n{RED}[!] No networks found. Try running with sudo/admin privileges.{RESET}\n")
        return

    # Sort by signal strength
    networks.sort(key=lambda x: float(str(x["dbm"]).split()[0]) if str(x["dbm"]).replace("-","").replace(".","").isdigit() else -100, reverse=True)

    print(f"\n{BOLD}{CYAN}{'─'*85}{RESET}")
    print(f"{BOLD}  {'#':<4} {'SSID':<28} {'Signal':<22} {'Quality':<14} {'Encryption':<18} {'Band'}{RESET}")
    print(f"{BOLD}{CYAN}{'─'*85}{RESET}")

    for i, net in enumerate(networks, 1):
        bars, quality = signal_bar(net["dbm"])
        enc_display   = encryption_color(net["security"])
        ssid_display  = (net["ssid"][:25] + "...") if len(net["ssid"]) > 28 else net["ssid"]
        freq          = net.get("freq", "N/A")
        band          = "5 GHz" if "5" in str(freq) else "2.4 GHz" if "2.4" in str(freq) or "24" in str(freq) else "N/A"

        print(f"  {BOLD}{i:<4}{RESET}{YELLOW}{ssid_display:<28}{RESET}{net['signal']:<22}{bars}  {quality:<6}  {enc_display:<18} {MAGENTA}{band}{RESET}")

    print(f"{BOLD}{CYAN}{'─'*85}{RESET}")
    print(f"\n{GREEN}✔ Total networks found: {len(networks)}{RESET}")


# ─────────────────────────────────────────────
# Save Report
# ─────────────────────────────────────────────
def save_report(networks):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"wifi_scan_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(f"WiFi Scan Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"GitHub: hemanathan115 | Tool #13 - WiFi Network Scanner\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"{'#':<4} {'SSID':<30} {'Signal':<20} {'Encryption':<20} {'BSSID'}\n")
        f.write("-" * 90 + "\n")
        for i, net in enumerate(networks, 1):
            f.write(f"{i:<4} {net['ssid']:<30} {str(net['signal']):<20} {net['security']:<20} {net.get('bssid','N/A')}\n")
        f.write(f"\nTotal: {len(networks)} networks scanned.\n")
    print(f"\n{GREEN}[✔] Report saved → {filename}{RESET}")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    print(BANNER)
    os_name = platform.system()
    print(f"{BLUE}[*] Detected OS: {os_name}{RESET}")
    print(f"{BLUE}[*] Scanning nearby WiFi networks...{RESET}\n")

    if os_name == "Linux":
        networks = scan_linux()
    elif os_name == "Darwin":
        networks = scan_macos()
    elif os_name == "Windows":
        networks = scan_windows()
    else:
        print(f"{RED}[!] Unsupported OS: {os_name}{RESET}")
        sys.exit(1)

    display_networks(networks)

    if networks:
        choice = input(f"\n{YELLOW}[?] Save scan report to file? (y/n): {RESET}").strip().lower()
        if choice == "y":
            save_report(networks)

    print(f"\n{CYAN}[*] Scan complete. Stay secure! 🔒{RESET}\n")


if __name__ == "__main__":
    main()
