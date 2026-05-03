# Script: day4_incident_analysis.py
# Author: Shivanand Sanglage
# Purpose: Analyse incident logs — find patterns, peak hours, worst hosts
# Day 4 of AIOps transition — Phase 1, Week 1

import pandas as pd
import numpy as np

#1. load

df= pd.read_csv("incidents.csv")
print("=" * 60)
print("  INCIDENT ANALYSIS REPORT")
print("=" * 60)
print(df.head())    
print(f" \n shape: {df.shape[0]} rows, {df.shape[1]} columns ") 
print(f" \n columns: {list(df.columns)} ")


#2. Clean

print("\n " +  "=" * 60)
print("  DATA QUALITY CHECKS")
print("-" * 60)

# Check for missing values

print(f"\n Missing values per column:")
print(df.isnull().sum())

# Check for duplicates
dupes = df.duplicated().sum()
print(f"\n Duplicate rows: {dupes}")

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Extract time features
df["hour"]        = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.day_name()
df["date"]        = df["timestamp"].dt.date
print(f"\n  Timestamp converted. Sample hours: {df['hour'].head().tolist()}")
print(f"  Date range: {df['date'].min()} → {df['date'].max()}")


#3. PEak Hour

print(f"\n " +  "=" * 60 )
print("  PEAK INCIDENT HOURS")
print("=" * 60)

hourly = df.groupby("hour")["id"].count().sort_values(ascending=False)

print(f"\n  Incidents by hour of day (top 5)")
for hour, count in hourly.head().items():
    bar = "█#" * count  # Scale bar length
    print(f"   Hour {hour:02d}:00 {bar:<20} {count} incidents")

#4. Worst Hosts

print(f"\n " +  "=" * 60 )
print("  WORST HOSTS BY INCIDENT COUNT")
print("=" * 60)

host_stats = df.groupby("host").agg(
    total_incidents = ("id",      "count"),
    p1_count        = ("severity", lambda x: (x == "P1").sum()),
    avg_duration    = ("duration_mins", "mean"),
    unresolved      = ("resolved",   lambda x: (x == "No").sum())
                      
).sort_values("p1_count", ascending=False)

print(f"\n {'HOST':<20} {'TOTAL':<7} {'P1s':>6} {'AVG_DUR':>10} {'UNRESOLVED':>12}")
print(f" {'-' *58}")
for host, row in host_stats.head().iterrows():
    print(f"    {host:<20} {row['total_incidents']:>7} "
          f"    {row['p1_count']:>6}  "
          f"    {row['avg_duration']:>9.1f}m  "
          f"    {row['unresolved']:>12}")

# ── 5. MTTR ANALYSIS

print(f"\n " +  "=" * 60 )
print("  MTTR ANALYSIS (Mean Time To Resolve)")
print("=" * 60)

# MTTR by severity

mttr_severity = df.groupby("severity")["duration_mins"].agg(
    mean_mins  = "mean",
    max_mins   = "max",
    min_mins   = "min",
    count      = "count"
).round(1)

print(f"\n  MTTR by severity:  \n")
print( f" {'SEVERITY':>10}  {'MEAN':>8}  {'MAX':>8}  {'MIN':>8}  {'COUNT':>8}")
print(f" {'-' *45}")
for sev, row in mttr_severity.iterrows():
    print(f" {sev:<10}  {row['mean_mins']:>7.1f}m  "
          f"{row['max_mins']:>7.1f}m   "
          f"{row['min_mins']:>7.1f}m  "
          f"{row['count']:>8}")

#6. MTTR by category
print(f"\n  MTTR by category: \n")
mttr_category = df.groupby("category")["duration_mins"].mean().sort_values(ascending=False)
for cat, mins in mttr_category.items():
    bar = "█#" * int(mins / 10)  # Scale bar length
    print(f"  {cat:<10} {bar:<25} {mins:>7.1f}m")

#7. Unresolved P1s — the most dangerous

print(f"\n  UNRESOLVED P1 INCIDENTS: \n")
unresolved_p1 = df[(df["severity"] == "P1") & (df["resolved"] == "No")]
if len("unresolved_p1") ==0:
    print("None,  All P1 incidents resolved. Great job!") 
else:
    for _, row in unresolved_p1.iterrows():
        print(f"  !!{row['host']:<20} Category: {row['category']:<10} "
        f"Duration: {row['duration_mins']} m"
        f" Date: {row['date']}")  

#8 INTELLIGENCE SUMMARY

print("\n " +  "=" * 60 )
print("  AIOPS INTELLIGENCE SUMMARY")
print("=" * 60)

total         = len(df)  # Total incidents
p1_total      = len(df[df["severity"] == "P1"])  # Total P1s 
unresolved_p1 = len(df[df["resolved"] == "No"])  # Unresolved P1s
peak_hour     = hourly.index[0]  # Peak hour
worst_host    = host_stats.index[0]  # Worst host
wrost_catt    = mttr_category.index[0]  # Worst category by MTTR
p1_rate       = round((p1_total / total) * 100, 1)  # P1 rate %
unres_rate    = round((unresolved_p1 / p1_total) * 100, 1)   # Unresolved P1 rate %

print(f""" 
      PERIOD ANALYSIS : {df['date'].min()} → {df['date'].max()}
      TOTAL INCIDENTS : {total}
      P1 RATE         : {p1_rate}% ({p1_total} of {total} incidents)
      UNRESOLVED RATE : {unres_rate}% ({unresolved_p1} of {p1_total} P1s)
      PEAK RISK HOUR  : {peak_hour:02d}:00 → staff NOC accordingly
      WORST HOST      : {worst_host} → {host_stats.loc[worst_host,'p1_count']:.0f} P1s, {host_stats.loc[worst_host,'unresolved']:.0f} unresolved
      WORST CATEGORY  : {wrost_catt} -> Avg {mttr_category[wrost_catt]:.1f} mins to resolve

      RECOMMENDATIONS:
  1. Investigate {worst_host} for permanent CPU fix — repeat offender
  2. Staff extra engineer at {peak_hour:02d}:00 — 9x incident spike
  3. Build runbook for {wrost_catt} incidents — longest MTTR category
  4. Review {unresolved_p1} unresolved P1s — SLA breach risk
""")
print("=" * 60)

  

























