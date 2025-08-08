#!/usr/bin/env python3
"""
F1 Telemetry Extractor using FastF1
Extracts telemetry data from F1 sessions
"""

import fastf1
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import logging

from config import Config
from models import TelemetryData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelemetryExtractor:
    """Extracts F1 telemetry data using FastF1"""
    
    def __init__(self, year: int, grand_prix: str, session_type: str):
        """Initialize the telemetry extractor"""
        self.year = year
        self.grand_prix = grand_prix
        self.session_type = session_type
        self.session = None
        
        # Enable FastF1 cache
        fastf1.Cache.enable_cache('cache')
        
    def load_session(self):
        """Load the F1 session data"""
        try:
            self.session = fastf1.get_session(self.year, self.grand_prix, self.session_type)
            self.session.load()
            logger.info(f"Loaded session: {self.year} {self.grand_prix} {self.session_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return False
    
    def get_drivers(self) -> List[Dict[str, str]]:
        """Get list of drivers in the session"""
        if not self.session:
            if not self.load_session():
                return []
        
        drivers = []
        for driver in self.session.drivers:
            driver_info = self.session.get_driver(driver)
            drivers.append({
                'driver_id': driver,
                'driver_name': driver_info['FullName'],
                'car_number': driver_info['CarNumber'],
                'team': driver_info['TeamName']
            })
        
        return drivers
    
    def extract_telemetry_for_driver(self, driver_id: str) -> List[TelemetryData]:
        """Extract telemetry data for a specific driver"""
        if not self.session:
            if not self.load_session():
                return []
        
        try:
            # Get driver info
            driver_info = self.session.get_driver(driver_id)
            
            # Get telemetry data
            telemetry = self.session.laps.pick_driver(driver_id).get_telemetry()
            
            if telemetry.empty:
                logger.warning(f"No telemetry data found for driver {driver_id}")
                return []
            
            # Convert to our format
            telemetry_data = []
            
            for idx, row in telemetry.iterrows():
                # Get lap info
                lap = self.session.laps.pick_driver(driver_id).iloc[0] if len(self.session.laps.pick_driver(driver_id)) > 0 else None
                
                # Create telemetry data point
                telemetry_point = TelemetryData(
                    timestamp=row.get('Time', datetime.now(timezone.utc)),
                    driver_id=driver_id,
                    driver_name=driver_info['FullName'],
                    car_number=driver_info['CarNumber'],
                    team=driver_info['TeamName'],
                    position=row.get('Position', 1),
                    lap_number=row.get('LapNumber', 1),
                    lap_time=row.get('LapTime', None),
                    sector1_time=row.get('Sector1Time', None),
                    sector2_time=row.get('Sector2Time', None),
                    sector3_time=row.get('Sector3Time', None),
                    speed=row.get('Speed', 0.0),
                    throttle=row.get('Throttle', 0.0),
                    brake=row.get('Brake', 0.0),
                    gear=row.get('Gear', 1),
                    rpm=row.get('RPM', 0),
                    drs=row.get('DRS', False),
                    coordinates={
                        'x': row.get('X', 0.0),
                        'y': row.get('Y', 0.0),
                        'z': row.get('Z', 0.0)
                    },
                    session_type=self.session_type,
                    year=self.year,
                    grand_prix=self.grand_prix
                )
                
                telemetry_data.append(telemetry_point)
            
            logger.info(f"Extracted {len(telemetry_data)} telemetry points for driver {driver_id}")
            return telemetry_data
            
        except Exception as e:
            logger.error(f"Error extracting telemetry for driver {driver_id}: {e}")
            return []
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get session information"""
        if not self.session:
            if not self.load_session():
                return {}
        
        return {
            'year': self.year,
            'grand_prix': self.grand_prix,
            'session_type': self.session_type,
            'track_name': self.session.track_name,
            'session_start': self.session.session_start_time,
            'session_end': self.session.session_end_time,
            'drivers': self.get_drivers()
        } 