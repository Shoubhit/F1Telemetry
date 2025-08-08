#!/usr/bin/env python3
"""
F1 Telemetry Kafka Consumer
Consumes messages from Kafka topics and stores in Cosmos DB
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any

from kafka import KafkaConsumer
from azure.cosmos import CosmosClient, PartitionKey

from config import Config
from models import TelemetryData, ControlMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class F1TelemetryConsumer:
    """Kafka consumer for F1 telemetry data"""
    
    def __init__(self):
        """Initialize Kafka consumer and Cosmos DB client"""
        # Initialize Kafka consumer
        self.consumer = KafkaConsumer(
            Config.KAFKA_TOPIC_TELEMETRY,
            Config.KAFKA_TOPIC_CONTROL,
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='f1-telemetry-consumer',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        # Initialize Cosmos DB client
        self.cosmos_client = CosmosClient(Config.COSMOS_ENDPOINT, Config.COSMOS_KEY)
        self.database = self.cosmos_client.create_database_if_not_exists(Config.COSMOS_DATABASE)
        self.container = self.database.create_container_if_not_exists(
            id=Config.COSMOS_CONTAINER,
            partition_key=PartitionKey(path="/driver_id")
        )
        
        logger.info("Kafka consumer and Cosmos DB client initialized")
    
    def store_telemetry_data(self, telemetry_data: Dict[str, Any]):
        """Store telemetry data in Cosmos DB"""
        try:
            # Add timestamp for Cosmos DB
            telemetry_data['id'] = f"{telemetry_data['driver_id']}_{telemetry_data['timestamp']}"
            telemetry_data['_ts'] = datetime.now().timestamp()
            
            # Store in Cosmos DB
            self.container.upsert_item(telemetry_data)
            logger.debug(f"Stored telemetry data for {telemetry_data['driver_id']}")
            
        except Exception as e:
            logger.error(f"Failed to store telemetry data: {e}")
    
    def process_control_message(self, control_data: Dict[str, Any]):
        """Process control messages"""
        try:
            action = control_data.get('action', '')
            logger.info(f"Processing control message: {action}")
            
            # You can add specific logic for different control actions here
            if action == 'start':
                logger.info("Simulation started")
            elif action == 'stop':
                logger.info("Simulation stopped")
            elif action == 'pause':
                logger.info("Simulation paused")
            elif action == 'speed':
                new_speed = control_data.get('data', {}).get('playback_speed', 1.0)
                logger.info(f"Playback speed changed to {new_speed}x")
                
        except Exception as e:
            logger.error(f"Failed to process control message: {e}")
    
    def consume_messages(self):
        """Consume messages from Kafka topics"""
        logger.info("Starting to consume messages from Kafka...")
        
        try:
            for message in self.consumer:
                topic = message.topic
                value = message.value
                
                logger.debug(f"Received message from topic {topic}")
                
                if topic == Config.KAFKA_TOPIC_TELEMETRY:
                    # Process telemetry data
                    self.store_telemetry_data(value)
                    
                elif topic == Config.KAFKA_TOPIC_CONTROL:
                    # Process control message
                    self.process_control_message(value)
                    
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
        finally:
            self.consumer.close()
            logger.info("Kafka consumer closed")
    
    def close(self):
        """Close the consumer connection"""
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer closed.")

def main():
    """Main function to run the consumer"""
    consumer = F1TelemetryConsumer()
    
    try:
        consumer.consume_messages()
    except KeyboardInterrupt:
        logger.info("Shutting down consumer...")
    finally:
        consumer.close()

if __name__ == "__main__":
    main() 