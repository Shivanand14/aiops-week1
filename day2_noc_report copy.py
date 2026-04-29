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
def risk_score(cpu, memory):
    return round((cpu * 0.6) + (memory * 0.4), 1)

def print_report(servers):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 70)
    print(f"  NOC TRIAGE REPORT  |  {now}")
    print("=" * 70)

    p1, p2, ok = [], [], []

    for s in servers:
        priority = triage(s["name"], s["cpu"], s["memory"])
        score = risk_score(s["cpu"], s["memory"])
        s["score"] = score
        if priority == "P1 CRITICAL":
            p1.append(s)
        elif priority == "P2 WARNING":
            p2.append(s)
        else:
            ok.append(s)

    # Sort P1 by risk score — highest risk first
    p1_sorted = sorted(p1, key=lambda x: x["score"], reverse=True)

    print(f"\n  TOP 5 HIGHEST RISK SERVERS (action first):")
    print(f"  {'SERVER':<22} {'CPU':>6} {'MEM':>6} {'RISK SCORE':>12}")
    print(f"  {'-'*50}")
    for s in p1_sorted[:5]:
        print(f"  {s['name']:<22} {s['cpu']:>5}% {s['memory']:>5}% {s['score']:>10}")

    print(f"\n  FULL REPORT:")
    for s in p1_sorted + p2 + ok:
        priority = triage(s["name"], s["cpu"], s["memory"])
        print(f"  {priority:<12} | {s['name']:<22} | CPU: {s['cpu']}%  MEM: {s['memory']}%  RISK: {s['score']}")

    print("\n" + "=" * 70)
    print(f"  SUMMARY  →  P1: {len(p1)}  |  P2: {len(p2)}  |  OK: {len(ok)}")
    # THIS BLOCK must be indented 4 spaces — inside the function
    p1_min_risk = min(s["score"] for s in p1) if p1 else 100
    risky_p2 = [s for s in p2 if s["score"] > p1_min_risk]

    if risky_p2:
        print(f"\n  RISK ALERT — {len(risky_p2)} P2 server(s) have higher risk than some P1s:")
        for s in risky_p2:
            print(f"  !! {s['name']:<22} RISK: {s['score']} — consider escalating to P1")

    print("\n" + "=" * 70)   # still inside function — 4 spaces indent
    
    
    

servers = load_servers("servers100.csv")
print_report(servers)

