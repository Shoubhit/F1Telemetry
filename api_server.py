#!/usr/bin/env python3
"""
FastAPI Server for F1 Telemetry
Provides REST API endpoints for the frontend
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from azure.cosmos import CosmosClient, PartitionKey
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="F1 Telemetry API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Cosmos DB client
cosmos_client = CosmosClient(Config.COSMOS_ENDPOINT, Config.COSMOS_KEY)
database = cosmos_client.create_database_if_not_exists(Config.COSMOS_DATABASE)
container = database.create_container_if_not_exists(
    id=Config.COSMOS_CONTAINER,
    partition_key=PartitionKey(path="/driver_id")
)

class TelemetryResponse(BaseModel):
    """Response model for telemetry data"""
    driver_id: str
    driver_name: str
    timestamp: datetime
    speed: float
    throttle: float
    brake: float
    gear: int
    rpm: int
    position: int
    lap_number: int

class DriverInfo(BaseModel):
    """Driver information model"""
    driver_id: str
    driver_name: str
    car_number: str
    team: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "F1 Telemetry API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/drivers", response_model=List[DriverInfo])
async def get_drivers():
    """Get list of all drivers"""
    try:
        # Query Cosmos DB for unique drivers
        query = "SELECT DISTINCT VALUE { 'driver_id': c.driver_id, 'driver_name': c.driver_name, 'car_number': c.car_number, 'team': c.team } FROM c"
        
        results = container.query_items(query=query, enable_cross_partition_query=True)
        drivers = [DriverInfo(**item) for item in results]
        
        return drivers
    except Exception as e:
        logger.error(f"Error getting drivers: {e}")
        raise HTTPException(status_code=500, detail="Failed to get drivers")

@app.get("/telemetry/{driver_id}", response_model=List[TelemetryResponse])
async def get_telemetry(driver_id: str, limit: int = 100):
    """Get telemetry data for a specific driver"""
    try:
        # Query Cosmos DB for telemetry data
        query = f"SELECT TOP {limit} c.driver_id, c.driver_name, c.timestamp, c.speed, c.throttle, c.brake, c.gear, c.rpm, c.position, c.lap_number FROM c WHERE c.driver_id = '{driver_id}' ORDER BY c.timestamp DESC"
        
        results = container.query_items(query=query, partition_key=driver_id)
        telemetry_data = [TelemetryResponse(**item) for item in results]
        
        return telemetry_data
    except Exception as e:
        logger.error(f"Error getting telemetry for driver {driver_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get telemetry for driver {driver_id}")

@app.get("/telemetry/{driver_id}/latest")
async def get_latest_telemetry(driver_id: str):
    """Get latest telemetry data for a specific driver"""
    try:
        # Query Cosmos DB for latest telemetry data
        query = f"SELECT TOP 1 c.driver_id, c.driver_name, c.timestamp, c.speed, c.throttle, c.brake, c.gear, c.rpm, c.position, c.lap_number FROM c WHERE c.driver_id = '{driver_id}' ORDER BY c.timestamp DESC"
        
        results = container.query_items(query=query, partition_key=driver_id)
        telemetry_data = list(results)
        
        if telemetry_data:
            return TelemetryResponse(**telemetry_data[0])
        else:
            raise HTTPException(status_code=404, detail=f"No telemetry data found for driver {driver_id}")
            
    except Exception as e:
        logger.error(f"Error getting latest telemetry for driver {driver_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get latest telemetry for driver {driver_id}")

@app.get("/telemetry/{driver_id}/stats")
async def get_driver_stats(driver_id: str):
    """Get statistics for a specific driver"""
    try:
        # Query for various statistics
        stats_query = f"""
        SELECT 
            c.driver_id,
            c.driver_name,
            MAX(c.speed) as max_speed,
            AVG(c.speed) as avg_speed,
            MAX(c.lap_number) as total_laps,
            MIN(c.timestamp) as session_start,
            MAX(c.timestamp) as session_end
        FROM c 
        WHERE c.driver_id = '{driver_id}'
        """
        
        results = container.query_items(query=stats_query, partition_key=driver_id)
        stats = list(results)
        
        if stats:
            return stats[0]
        else:
            raise HTTPException(status_code=404, detail=f"No data found for driver {driver_id}")
            
    except Exception as e:
        logger.error(f"Error getting stats for driver {driver_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats for driver {driver_id}")

@app.get("/session/info")
async def get_session_info():
    """Get current session information"""
    try:
        # Query for session information
        session_query = """
        SELECT DISTINCT VALUE {
            'year': c.year,
            'grand_prix': c.grand_prix,
            'session_type': c.session_type
        } FROM c
        """
        
        results = container.query_items(query=session_query, enable_cross_partition_query=True)
        session_info = list(results)
        
        if session_info:
            return session_info[0]
        else:
            return {"year": Config.DEFAULT_YEAR, "grand_prix": Config.DEFAULT_GRAND_PRIX, "session_type": Config.DEFAULT_SESSION}
            
    except Exception as e:
        logger.error(f"Error getting session info: {e}")
        return {"year": Config.DEFAULT_YEAR, "grand_prix": Config.DEFAULT_GRAND_PRIX, "session_type": Config.DEFAULT_SESSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.API_HOST, port=Config.API_PORT) 