# Script: day3_baseline.py
# Author: Shivanand Sanglage
# Purpose: Statistical baselining — detect anomalies using mean + std
# Day 3 of AIOps transition — Phase 1, Week 1

import numpy as np

# Simulate 30 days of hourly CPU readings for 3 different servers
# Each server has its own "normal" behaviour pattern

def detect_trend(history, window=24):
    # Look at last 24 hours vs previous 24 hours
    # If rising fast — flag it before it breaches threshold
    # Simple linear regression to detect upward trends

    recent = np.mean(history[-window:])
    previous = np.mean(history[-2*window:-window])
    change = recent - previous

    if change > 10:  # Arbitrary threshold for "rising fast"
        return f" RISING FAST (+{change:.1f}%)"
    elif change < 5:
        return f" RISING (+{change:.1f}%)"
    elif change < -10:
        return f" DROPPING ({change:.1f}%)"
    else:        
        return f" STABLE ({change:+.1f}%)"

    

def time_to_breach(history, threshold, window=24, current_override=None):
    # Estimate how many hours until we breach threshold based on recent trend
    # Simple linear extrapolation to estimate when we might breach threshold
    recent = np.mean(history[-window:])
    previous = np.mean(history[-2*window:-window])
    hourly_rate = (recent - previous) / window  # Change per hour

    if hourly_rate <= 0:
        return None
    current = current_override if current_override is not None else history[-1]
    
    if current >= threshold:
        return 0
    hours = (threshold - current) / hourly_rate 
    return round(hours, 1)

    

np.random.seed(42)

# Base normal history — 696 hours (29 days)
base_db = np.random.normal(loc=75, scale=5,  size=696)  # High CPU server
base_web = np.random.normal(loc=15, scale=8,  size=696)  # Low CPU server
base_cache = np.random.normal(loc=45, scale=6, size=696)  # Moderate CPU server

# Last 24 hours — inject a rising trend
rising_db = np.linspace(75, 92, 24)  # Rising trend
rising_web = np.linspace(15, 33, 24)  # Rising trend
rising_cache = np.linspace(45, 119, 24)  # Rising trend

servers = {
    "prod-db-01":  np.clip(np.concatenate([base_db, rising_db]), 0, 100),
    "prod-web-01": np.clip(np.concatenate([base_web, rising_web]), 0, 100),
    "prod-cache-01": np.clip(np.concatenate([base_cache, rising_cache]), 0, 100),
}

# Clip values to realistic range 0-100

for name in servers:
    servers[name] = np.clip(servers[name], 0, 100)

# Today's readings — one current value per server

todays_readings = {  
    "prod-db-01": 87.0,  # Anomalous high
    "prod-web-01": 87.0, # Normal low
    "prod-cache-01": 87.0 # Normal
}

print("=" * 60)
print("  STATISTICAL BASELINE ANOMALY REPORT")
print("=" * 70)
print(f"  {'SERVER':<20} {'Mean':>8} {'STD':>8} {'THRESHOLD':>12} {'NOW' :8} {'STATUS':>12}")
print(f" {'-'*65}")

for name, history in servers.items():
    mean = np.mean(history)
    std = np.std(history)
    p1_thresh = mean + (3 * std)
    p2_thresh = mean + (2 * std)
    current = todays_readings[name]
    trend = detect_trend(history)
    ttb = time_to_breach(history, p1_thresh, current_override=current)
    if ttb is None:
        ttb_msg = "Not breaching"
    elif ttb == 0:
        ttb_msg = "Already breached"
    else:
        ttb_msg = f"Breaches in {ttb} hrs"
    

    if current > p1_thresh:
       status = "CRITICAL"
    elif current > p2_thresh:
       status = "WARNING"   
    else:
       status = "OK"
    print(f"{name:<20}|{current:<7.1f}|{mean:<7.1f}|{std:<7.1f}|{status:<12}|{trend}| {ttb_msg} ")

print("=" * 70)

