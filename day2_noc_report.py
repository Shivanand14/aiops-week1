# Script: day2_noc_report.py
# Author: Shivanand Sanglage
# Purpose: Read server data from CSV, triage all servers, print NOC report
# Day 2 of AIOps transition — Phase 1, Week 1


import csv
from datetime import datetime

def triage(name, cpu, memory):
    

    if cpu > 85 or memory > 90:
        return  "P1 CRITICAL"
    elif cpu > 75 or memory > 75:
        return  "P2 WARNING"
    else:
        return "OK"
    
def load_servers (filename):
     servers = []
     with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            servers.append({
                "name": row["name"],
                "cpu": float(row["cpu"]),
                "memory": float(row["memory"])
            })
     return servers
def print_report(servers):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("=" * 65)
    print(f"  NOC REPORT |  {now}")
    print("=" * 65)

    p1,p2,ok = [],[],[]

    for s in servers:
        priority = triage(s["name"], s["cpu"], s["memory"])
        print(f"{priority:<12} | {s['name']:<20} | CPU: {s['cpu']}%  memory: {s['memory']}%") 
        if priority == "P1 CRITICAL":
            p1.append(s["name"])
        elif priority == "P2 WARNING":
            p2.append(s["name"])
        else:
            ok.append(s["name"])

    print("=" * 65)
    print(f"  SUMMARY →  P1: {len(p1)}  |  P2: {len(p2)}  |  OK: {len(ok)}")
    print("=" * 65)

    if p1:
      print("\n  Action required:   ")
      for name in p1:
          print(f" - Page on call Engineer for:  {name}")

servers = load_servers("servers100.csv")
print_report(servers)

