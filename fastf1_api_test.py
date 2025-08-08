#!/usr/bin/env python3
"""
Test script to explore FastF1 API for timing and distance calculations
"""

import fastf1

session = fastf1.get_session(2023, 'Monza', 'R')
session.load()
ver_data = session.laps.pick_drivers('VER').pick_fastest()
tel = ver_data.get_telemetry()

tel["Time_seconds"] = tel["Time"].dt.total_seconds()

print("Time in seconds:", tel["Time_seconds"].iloc[0])


