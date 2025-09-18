#!/usr/bin/env python3
import platform
import subprocess
import socket
import json
import os
import shutil
import sys

WORKER = os.path.join(os.path.dirname(__file__), "nmap_worker.py")


def _run_cmd_and_get_json(cmd, timeout=600):
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Nmap worker timed out.")
    if proc.returncode != 0:
        stderr = proc.stderr.decode(errors="ignore").strip()
        raise RuntimeError(stderr or f"Command failed with code {proc.returncode}")
    out = proc.stdout.decode(errors="ignore").strip()
    if not out:
        return []
    try:
        return json.loads(out)
    except Exception as e:
        raise RuntimeError(f"Failed to parse worker output: {e}\nOutput: {out}")


def run_nmap_with_privileges(prefix):
    system = platform.system()
    if system == "Windows":
        cmd = [sys.executable, "-u", WORKER, prefix]
        return _run_cmd_and_get_json(cmd)

    if shutil.which("pkexec"):
        cmd = ["pkexec", sys.executable, "-u", WORKER, prefix]
        return _run_cmd_and_get_json(cmd)
    if shutil.which("sudo"):
        cmd = ["sudo", sys.executable, "-u", WORKER, prefix]
        return _run_cmd_and_get_json(cmd)
    raise PermissionError(
        "Cannot elevate privileges automatically. Use pkexec or sudo."
    )


def get_local_prefix():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        prefix = ".".join(ip.split(".")[:-1]) + ".0/24"
        return prefix
    finally:
        s.close()


def get_mac(ip):
    system = platform.system()
    try:
        if system == "Linux":
            proc = subprocess.Popen(["ip", "neigh", "show", ip], stdout=subprocess.PIPE)
            out, _ = proc.communicate(timeout=2)
            line = out.decode().strip()
            if "lladdr" in line:
                return line.split("lladdr")[1].split()[0]
        elif system == "Darwin":
            proc = subprocess.Popen(["arp", "-n", ip], stdout=subprocess.PIPE)
            out, _ = proc.communicate(timeout=2)
            parts = out.decode().split()
            if len(parts) >= 4:
                return parts[3]
        elif system == "Windows":
            proc = subprocess.Popen(["arp", "-a", ip], stdout=subprocess.PIPE)
            out, _ = proc.communicate(timeout=2)
            for line in out.decode().splitlines():
                if ip in line:
                    cols = line.split()
                    if len(cols) >= 2:
                        return cols[1]
    except Exception:
        return "Unknown"
    return "Unknown"


def scan_network():
    try:
        prefix = get_local_prefix()
    except Exception:
        raise RuntimeError("Failed to determine local IP/network prefix.")

    devices = run_nmap_with_privileges(prefix)
    for device in devices:
        device_ip = device.get("ip", "")
        device["mac"] = get_mac(device_ip) if device_ip else "Unknown"
        device["vendor"] = str(device.get("vendor", ""))
        device["os"] = str(device.get("os", ""))
        device["hostname"] = str(device.get("hostname", ""))
    return devices
