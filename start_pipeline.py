#!/usr/bin/env python3
"""
F1 Telemetry Pipeline Orchestrator
Starts all components of the F1 Telemetry Pipeline
"""

import asyncio
import logging
import subprocess
import sys
import time
from typing import List, Dict, Any
import threading

from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class F1TelemetryPipeline:
    """Orchestrates the F1 Telemetry Pipeline"""
    
    def __init__(self):
        """Initialize the pipeline orchestrator"""
        self.processes = {}
        self.running = False
        
    def start_kafka_services(self):
        """Start Kafka and Zookeeper using Docker Compose"""
        try:
            logger.info("Starting Kafka services with Docker Compose...")
            subprocess.run(["docker-compose", "up", "-d"], check=True)
            logger.info("Kafka services started successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start Kafka services: {e}")
            return False
        except FileNotFoundError:
            logger.error("Docker Compose not found. Please install Docker Desktop.")
            return False
    
    def start_kafka_consumer(self):
        """Start the Kafka consumer process"""
        try:
            logger.info("Starting Kafka consumer...")
            process = subprocess.Popen([sys.executable, "kafka_consumer.py"])
            self.processes['kafka_consumer'] = process
            logger.info("Kafka consumer started")
            return True
        except Exception as e:
            logger.error(f"Failed to start Kafka consumer: {e}")
            return False
    
    def start_websocket_server(self):
        """Start the WebSocket server process"""
        try:
            logger.info("Starting WebSocket server...")
            process = subprocess.Popen([sys.executable, "websocket_server.py"])
            self.processes['websocket_server'] = process
            logger.info("WebSocket server started")
            return True
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
            return False
    
    def start_api_server(self):
        """Start the FastAPI server process"""
        try:
            logger.info("Starting API server...")
            process = subprocess.Popen([sys.executable, "api_server.py"])
            self.processes['api_server'] = process
            logger.info("API server started")
            return True
        except Exception as e:
            logger.error(f"Failed to start API server: {e}")
            return False
    
    def start_frontend(self):
        """Start the Next.js frontend"""
        try:
            logger.info("Starting Next.js frontend...")
            process = subprocess.Popen(["npm", "run", "dev"], cwd="frontend")
            self.processes['frontend'] = process
            logger.info("Frontend started")
            return True
        except Exception as e:
            logger.error(f"Failed to start frontend: {e}")
            return False
    
    def run_telemetry_simulation(self):
        """Run the telemetry simulation"""
        try:
            logger.info("Starting telemetry simulation...")
            process = subprocess.Popen([sys.executable, "kafka_producer.py"])
            self.processes['telemetry_simulation'] = process
            logger.info("Telemetry simulation started")
            return True
        except Exception as e:
            logger.error(f"Failed to start telemetry simulation: {e}")
            return False
    
    def wait_for_services(self):
        """Wait for services to be ready"""
        logger.info("Waiting for services to be ready...")
        time.sleep(10)  # Give services time to start
        logger.info("Services should be ready now")
    
    def start_pipeline(self):
        """Start the complete F1 Telemetry Pipeline"""
        logger.info("🏎️ Starting F1 Telemetry Pipeline...")
        
        # Start Kafka services
        if not self.start_kafka_services():
            logger.error("Failed to start Kafka services. Exiting.")
            return False
        
        # Wait for Kafka to be ready
        logger.info("Waiting for Kafka to be ready...")
        time.sleep(15)
        
        # Start backend services
        services_started = True
        services_started &= self.start_kafka_consumer()
        services_started &= self.start_websocket_server()
        services_started &= self.start_api_server()
        
        if not services_started:
            logger.error("Failed to start some backend services. Exiting.")
            return False
        
        # Wait for backend services
        self.wait_for_services()
        
        # Start frontend
        if not self.start_frontend():
            logger.warning("Failed to start frontend. You can start it manually with: cd frontend && npm run dev")
        
        # Start telemetry simulation
        if not self.run_telemetry_simulation():
            logger.warning("Failed to start telemetry simulation. You can start it manually with: python kafka_producer.py")
        
        self.running = True
        logger.info("🎉 F1 Telemetry Pipeline started successfully!")
        logger.info("📊 Access points:")
        logger.info("   - Frontend: http://localhost:3000")
        logger.info("   - API Server: http://localhost:8000")
        logger.info("   - WebSocket: ws://localhost:8765")
        logger.info("   - Kafka UI: http://localhost:8080")
        
        return True
    
    def stop_pipeline(self):
        """Stop the F1 Telemetry Pipeline"""
        logger.info("🛑 Stopping F1 Telemetry Pipeline...")
        
        # Stop all processes
        for name, process in self.processes.items():
            try:
                logger.info(f"Stopping {name}...")
                process.terminate()
                process.wait(timeout=10)
                logger.info(f"{name} stopped")
            except subprocess.TimeoutExpired:
                logger.warning(f"{name} did not stop gracefully, forcing...")
                process.kill()
            except Exception as e:
                logger.error(f"Error stopping {name}: {e}")
        
        # Stop Docker services
        try:
            logger.info("Stopping Docker services...")
            subprocess.run(["docker-compose", "down"], check=True)
            logger.info("Docker services stopped")
        except Exception as e:
            logger.error(f"Error stopping Docker services: {e}")
        
        self.running = False
        logger.info("Pipeline stopped")
    
    def monitor_pipeline(self):
        """Monitor the pipeline and restart failed services"""
        while self.running:
            try:
                for name, process in self.processes.items():
                    if process.poll() is not None:
                        logger.warning(f"{name} has stopped unexpectedly")
                        # You could add logic here to restart failed services
                
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                logger.info("Received interrupt signal")
                break
            except Exception as e:
                logger.error(f"Error monitoring pipeline: {e}")

def main():
    """Main function to run the pipeline"""
    pipeline = F1TelemetryPipeline()
    
    try:
        # Start the pipeline
        if pipeline.start_pipeline():
            # Monitor the pipeline
            pipeline.monitor_pipeline()
        else:
            logger.error("Failed to start pipeline")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        pipeline.stop_pipeline()

if __name__ == "__main__":
    main() 