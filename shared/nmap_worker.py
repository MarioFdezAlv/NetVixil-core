#!/usr/bin/env python3
import nmap
import sys
import json

if len(sys.argv) < 2:
    print(json.dumps([]))
    sys.exit(0)

prefix = sys.argv[1]
nm = nmap.PortScanner()
nm.scan(hosts=prefix, arguments="-Pn -O -sS")

devices = []
for host in nm.all_hosts():
    os_name = ""
    if "osmatch" in nm[host] and nm[host]["osmatch"]:
        os_name = nm[host]["osmatch"][0]["name"]

    vendor = ""
    if "vendor" in nm[host]:
        vendor = nm[host]["vendor"]

    device = {
        "ip": host,
        "hostname": nm[host].hostname() or "",
        "vendor": vendor,
        "os": os_name,
    }

    devices.append(device)

print(json.dumps(devices))
