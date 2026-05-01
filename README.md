# AIOps Week 1 — Server Triage Engine

Built during my AIOps transition from 13 years of IT Operations.

## What this does
Reads server metrics from CSV, triages all servers into P1/P2/OK 
priority using risk scoring, and flags under-classified servers 
that static thresholds would miss.

## Scripts
 `day1_triage.py` — Day 1: basic triage logic with if/else
 `generate_servers.py` — generates 100 simulated servers
 `day2_noc_report.py` — full NOC report with risk scoring

## How to run
pip install -r requirements.txt
python generate_servers.py
python day2_noc_report.py

## Key concept
Static thresholds miss dangerous servers. Risk scoring catches 
servers where combined CPU + memory pressure exceeds any single 
P1 threshold. Found 14 under-classified servers in 100-server test.

Memory exhaustion cascades to full outage via OOM killer.
CPU spikes cause degradation but are often self-recovering.
Therefore: prod-db-* servers weight memory at 0.6, CPU at 0.4.

## Author
Shivanand Sanglage — 13 years IT Operations → AIOps Engineer
https://www.linkedin.com/in/shivanand-sanglage-4a036350/
https://github.com/Shivanand14
