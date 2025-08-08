#!/usr/bin/env python3
"""
F1 Telemetry Kafka Producer
Sends telemetry and control messages to Kafka topics
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

from kafka import KafkaProducer
from kafka.errors import KafkaError

from config import Config
from models import TelemetryData, ControlMessage
from telemetry_extractor import TelemetryExtractor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class F1TelemetryProducer:
    """Kafka producer for F1 telemetry data"""
    
    def __init__(self):
        """Initialize Kafka producer"""
        self.producer = KafkaProducer(
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(0, 10, 1)
        )
        logger.info(f"Kafka producer initialized for servers: {Config.KAFKA_BOOTSTRAP_SERVERS}")

    def send_telemetry_data(self, telemetry_data: TelemetryData):
        """Send telemetry data to Kafka topic"""
        try:
            self.producer.send(Config.KAFKA_TOPIC_TELEMETRY, telemetry_data.model_dump()).get(timeout=10)
            logger.debug(f"Sent telemetry for {telemetry_data.driver_id} at {telemetry_data.timestamp}")
        except KafkaError as e:
            logger.error(f"Failed to send telemetry data: {e}")

    def send_control_message(self, message: ControlMessage):
        """Send control message to Kafka topic"""
        try:
            self.producer.send(Config.KAFKA_TOPIC_CONTROL, message.model_dump()).get(timeout=10)
            logger.info(f"Sent control message: {message.action}")
        except KafkaError as e:
            logger.error(f"Failed to send control message: {e}")

    def close(self):
        """Close the producer connection"""
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed.")

class TelemetrySimulator:
    """Simulates F1 telemetry by replaying historical data"""
    
    def __init__(self):
        """Initialize the simulator"""
        self.producer = F1TelemetryProducer()
        self.extractor = TelemetryExtractor(
            year=Config.DEFAULT_YEAR,
            grand_prix=Config.DEFAULT_GRAND_PRIX,
            session_type=Config.DEFAULT_SESSION
        )
    
    async def simulate_telemetry_stream(self, driver_id: str, playback_speed: float = 1.0):
        """Simulate telemetry stream for a driver"""
        try:
            # Load telemetry data
            telemetry_points = self.extractor.extract_telemetry_for_driver(driver_id)
            logger.info(f"Loaded {len(telemetry_points)} telemetry points for driver {driver_id}")

            if not telemetry_points:
                logger.warning(f"No telemetry data found for driver {driver_id}. Exiting simulation.")
                return

            # Send start control message
            start_message = ControlMessage(
                timestamp=datetime.now(timezone.utc),
                action="start",
                data={"driver_id": driver_id, "playback_speed": playback_speed}
            )
            self.producer.send_control_message(start_message)

            # Simulate real-time streaming
            for i, point in enumerate(telemetry_points):
                self.producer.send_telemetry_data(point)
                
                # Calculate sleep time based on playback speed and time difference between points
                if i < len(telemetry_points) - 1:
                    time_diff = (telemetry_points[i+1].timestamp - point.timestamp).total_seconds()
                    sleep_duration = time_diff / playback_speed
                    await asyncio.sleep(max(0, sleep_duration))

            # Send stop control message
            stop_message = ControlMessage(
                timestamp=datetime.now(timezone.utc),
                action="stop",
                data={"driver_id": driver_id}
            )
            self.producer.send_control_message(stop_message)
            logger.info(f"Simulation for driver {driver_id} completed.")

        except Exception as e:
            logger.error(f"Error during telemetry simulation: {e}")
        finally:
            self.producer.close()

async def main():
    """Main function to run the telemetry simulation"""
    simulator = TelemetrySimulator()
    
    # You can change the default driver and playback speed here
    driver_to_simulate = Config.DEFAULT_DRIVER
    playback_speed = Config.DEFAULT_PLAYBACK_SPEED
    
    logger.info(f"Starting F1 Telemetry Simulation for driver {driver_to_simulate} at {playback_speed}x speed...")
    await simulator.simulate_telemetry_stream(driver_to_simulate, playback_speed)
    logger.info("F1 Telemetry Simulation finished.")

if __name__ == "__main__":
    asyncio.run(main()) 