# generate_servers.py
# Generates 100 fake servers with random CPU and memory values

import csv
import random

random.seed(42)

server_types = [
    "prod-db", "prod-web", "prod-cache", "prod-api",
    "prod-auth", "prod-queue", "prod-billing", "prod-search",
    "neustar-oms", "yesmail-smtp"
]

with open("servers100.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["name", "cpu", "memory"])

    for i in range(1, 101):
        server_type = random.choice(server_types)
        name = f"{server_type}-{i:02d}"
        cpu = round(random.uniform(20, 100), 1)
        memory = round(random.uniform(20, 100), 1)
        writer.writerow([name, cpu, memory])