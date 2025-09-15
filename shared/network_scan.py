import socket
import subprocess
import platform
import nmap
import uuid
import re


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def scan_network(network_prefix=None):
    """
    Scan the local network and return a list of devices with details.
    """
    devices = []
    local_ip = get_local_ip()
    if not network_prefix:
        network_prefix = ".".join(local_ip.split(".")[:3]) + ".0/24"

    nm = nmap.PortScanner()
    nm.scan(hosts=network_prefix, arguments="-O -sS -p 1-1024")

    for host in nm.all_hosts():
        device = {}
        device["ip"] = host
        device["hostname"] = nm[host].hostname() or host
        device["state"] = nm[host].state()
        try:
            device["os"] = nm[host]["osmatch"][0]["name"]
        except:
            device["os"] = "Unknown"
        ports = []
        try:
            for proto in nm[host].all_protocols():
                for port in nm[host][proto].keys():
                    ports.append(
                        {
                            "port": port,
                            "state": nm[host][proto][port]["state"],
                            "service": nm[host][proto][port]["name"],
                        }
                    )
        except:
            ports = []
        device["ports"] = ports
        device["mac"] = get_mac(host)
        device["vendor"] = get_vendor(device["mac"])
        devices.append(device)
    return devices


def get_mac(ip):
    """
    Get MAC address using ARP.
    """
    if platform.system() == "Windows":
        pid = subprocess.Popen(["arp", "-a", ip], stdout=subprocess.PIPE)
        s = pid.communicate()[0].decode()
        match = re.search(r"([0-9a-f]{2}[-:]){5}[0-9a-f]{2}", s, re.I)
        return match.group(0) if match else None
    else:
        pid = subprocess.Popen(["arp", "-n", ip], stdout=subprocess.PIPE)
        s = pid.communicate()[0].decode()
        match = re.search(r"(([0-9a-f]{1,2}[:]){5}[0-9a-f]{1,2})", s, re.I)
        return match.group(0) if match else None


def get_vendor(mac):
    """
    Simple MAC vendor lookup using the first 3 octets.
    """
    if not mac:
        return None
    mac_prefix = mac.upper().replace("-", ":")[:8]
    # For now, return prefix; later can integrate with IEEE OUI database
    return mac_prefix
