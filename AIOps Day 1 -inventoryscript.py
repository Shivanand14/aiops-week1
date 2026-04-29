servers = [

 {"name": "prod-db-01",  "cpu": 92.5, "memory": 88.0},
    {"name": "prod-web-01", "cpu": 45.0, "memory": 99.0},
    {"name": "prod-cache-01","cpu": 78.2, "memory": 45.5},
    {"name": "neustar-oms-01","cpu": 90, "memory": 95.0},
    {"name": "prod-api-01", "cpu": 55.0, "memory": 72.0}

]

def triage(server):
    cpu = server["cpu"]
    memory = server["memory"]
    Name = server["name"]

    if cpu > 85 or memory > 90:
        priority = "P1 CRITICAL"
    elif cpu > 75 or memory > 75:
        priority =  "P2 WARNING"
    else:
        return "OK"
    return f"{priority:<12} | {Name:<20} | CPU: {cpu}%  memory: {memory}%"

print("=" * 60)
print("  SERVER TRIAGE REPORT")
print("=" * 60)
for s in servers:
    print(triage(s)) 
print("=" * 60)
p1_servers = [s for s in servers if s["cpu"] > 85 or s["memory"] > 90]
p2_servers = [s for s in servers if s not in p1_servers 
              and (70 < s["cpu"] <= 85 or 80 < s["memory"] <= 90)]
ok_servers  = [s for s in servers if s not in p1_servers 
              and s not in p2_servers]

p1_count = len(p1_servers)
p2_count = len(p2_servers)
ok_count  = len(ok_servers)

print(f"  SUMMARY →  P1: {p1_count}  |  P2: {p2_count}  |  OK: {ok_count}")
print("=" * 60)

