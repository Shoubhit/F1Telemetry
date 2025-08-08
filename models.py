from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class TelemetryData(BaseModel):
    """F1 Telemetry Data Model"""
    timestamp: datetime
    driver_id: str
    driver_name: str
    car_number: str
    team: str
    position: int
    lap_number: int
    lap_time: Optional[float] = None
    sector1_time: Optional[float] = None
    sector2_time: Optional[float] = None
    sector3_time: Optional[float] = None
    speed: float
    throttle: float
    brake: float
    gear: int
    rpm: int
    drs: bool
    coordinates: Dict[str, float] = Field(default_factory=dict)
    session_type: str
    year: int
    grand_prix: str

class SimulationState(BaseModel):
    """Simulation State Model"""
    is_running: bool = False
    current_time: Optional[datetime] = None
    playback_speed: float = 1.0
    current_driver: str = "VER"
    session_info: Dict[str, Any] = Field(default_factory=dict)

class ControlMessage(BaseModel):
    """Control Message Model"""
    action: str  # 'start', 'stop', 'pause', 'reset', 'speed'
    timestamp: datetime = Field(default_factory=datetime.now)
    data: Optional[Dict[str, Any]] = None

class RacePosition(BaseModel):
    """Race Position Model"""
    driver_id: str
    driver_name: str
    car_number: str
    team: str
    position: int
    lap_number: int
    lap_time: Optional[float] = None
    gap_to_leader: Optional[float] = None
    last_lap_time: Optional[float] = None
    best_lap_time: Optional[float] = None
    sector1_time: Optional[float] = None
    sector2_time: Optional[float] = None
    sector3_time: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now) 