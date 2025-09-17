#!/usr/bin/env python3
"""
parse_logs.py
Simple parser for the mini-ssh-honeypot's JSONL log file (honeypot.log).

Produces:
 - auth_attempts.csv  (timestamp, src_ip, src_port, username, password, result)
 - commands.csv       (timestamp, src_ip, src_port, username, command)

Usage:
  python parse_logs.py           # reads honeypot.log in cwd
  python parse_logs.py path/to/honeypot.log
"""

import json
import csv
import sys
from collections import Counter
from pathlib import Path

DEFAULT_LOG = "honeypot.log"
AUTH_CSV = "auth_attempts.csv"
CMD_CSV = "commands.csv"

def load_events(path):
    events = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                # skip malformed lines but report count
                print(f"[!] Skipped invalid JSON at line {lineno}")
    return events

def export_auths(events, outpath=AUTH_CSV):
    auths = [e for e in events if e.get("type") == "auth_attempt"]
    with open(outpath, "w", newline="", encoding="utf-8") as csvf:
        w = csv.writer(csvf)
        w.writerow(["timestamp", "src_ip", "src_port", "username", "password", "result"])
        for a in auths:
            w.writerow([
                a.get("timestamp"),
                a.get("src_ip"),
                a.get("src_port"),
                a.get("username"),
                a.get("password"),
                a.get("result", "")
            ])
    return auths

def export_cmds(events, outpath=CMD_CSV):
    cmds = [e for e in events if e.get("type") == "command"]
    with open(outpath, "w", newline="", encoding="utf-8") as csvf:
        w = csv.writer(csvf)
        w.writerow(["timestamp", "src_ip", "src_port", "username", "command"])
        for c in cmds:
            w.writerow([
                c.get("timestamp"),
                c.get("src_ip"),
                c.get("src_port"),
                c.get("username"),
                c.get("command")
            ])
    return cmds

def print_summary(auths, cmds):
    print("=== Honeypot Summary ===")
    print(f"Total auth attempts: {len(auths)}")
    print(f"Total commands captured: {len(cmds)}")
    top_users = Counter(a.get("username") for a in auths).most_common(10)
    top_pwds  = Counter(a.get("password") for a in auths).most_common(10)
    top_ips   = Counter(a.get("src_ip") for a in auths).most_common(10)

    if top_users:
        print("\nTop usernames attempted:")
        for u,c in top_users:
            print(f"  {u} - {c}")
    if top_pwds:
        print("\nTop passwords attempted:")
        for p,c in top_pwds:
            print(f"  {p} - {c}")
    if top_ips:
        print("\nTop source IPs:")
        for ip,c in top_ips:
            print(f"  {ip} - {c}")

def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(DEFAULT_LOG)
    if not path.exists():
        print(f"[!] Log file not found: {path.resolve()}")
        sys.exit(1)

    events = load_events(path)
    auths = export_auths(events)
    cmds  = export_cmds(events)
    print_summary(auths, cmds)
    print(f"\nWrote: {AUTH_CSV} ({len(auths)} rows), {CMD_CSV} ({len(cmds)} rows)")

if __name__ == "__main__":
    main()
