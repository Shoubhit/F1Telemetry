#!/usr/bin/env python3
"""
WebSocket Server for F1 Telemetry
Provides real-time telemetry data to frontend clients
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Set, Any

import websockets
from kafka import KafkaConsumer

from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class F1TelemetryWebSocketServer:
    """WebSocket server for F1 telemetry data"""
    
    def __init__(self):
        """Initialize WebSocket server"""
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.kafka_consumer = None
        
    async def register_client(self, websocket: websockets.WebSocketServerProtocol):
        """Register a new WebSocket client"""
        self.clients.add(websocket)
        logger.info(f"New client connected. Total clients: {len(self.clients)}")
        
        # Send welcome message
        welcome_message = {
            "type": "connection",
            "message": "Connected to F1 Telemetry WebSocket Server",
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send(json.dumps(welcome_message))
    
    async def unregister_client(self, websocket: websockets.WebSocketServerProtocol):
        """Unregister a WebSocket client"""
        self.clients.discard(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def broadcast_telemetry(self, telemetry_data: Dict[str, Any]):
        """Broadcast telemetry data to all connected clients"""
        if not self.clients:
            return
        
        message = {
            "type": "telemetry",
            "data": telemetry_data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Send to all connected clients
        disconnected_clients = set()
        for client in self.clients:
            try:
                await client.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                logger.error(f"Error sending to client: {e}")
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            await self.unregister_client(client)
    
    async def broadcast_control(self, control_data: Dict[str, Any]):
        """Broadcast control messages to all connected clients"""
        if not self.clients:
            return
        
        message = {
            "type": "control",
            "data": control_data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Send to all connected clients
        disconnected_clients = set()
        for client in self.clients:
            try:
                await client.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                logger.error(f"Error sending to client: {e}")
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            await self.unregister_client(client)
    
    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle individual WebSocket client"""
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    logger.debug(f"Received message from client: {data}")
                    
                    # Handle client messages (e.g., subscription requests)
                    if data.get("type") == "subscribe":
                        # Handle subscription logic here
                        response = {
                            "type": "subscription",
                            "status": "subscribed",
                            "timestamp": datetime.now().isoformat()
                        }
                        await websocket.send(json.dumps(response))
                        
                except json.JSONDecodeError:
                    logger.warning("Received invalid JSON from client")
                except Exception as e:
                    logger.error(f"Error handling client message: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client connection closed")
        except Exception as e:
            logger.error(f"Error in client handler: {e}")
        finally:
            await self.unregister_client(websocket)
    
    async def kafka_consumer_task(self):
        """Task to consume messages from Kafka and broadcast to WebSocket clients"""
        try:
            self.kafka_consumer = KafkaConsumer(
                Config.KAFKA_TOPIC_TELEMETRY,
                Config.KAFKA_TOPIC_CONTROL,
                bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
                auto_offset_reset='latest',
                enable_auto_commit=True,
                group_id='websocket-consumer',
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            
            logger.info("Kafka consumer started for WebSocket server")
            
            for message in self.kafka_consumer:
                topic = message.topic
                value = message.value
                
                if topic == Config.KAFKA_TOPIC_TELEMETRY:
                    await self.broadcast_telemetry(value)
                elif topic == Config.KAFKA_TOPIC_CONTROL:
                    await self.broadcast_control(value)
                    
        except Exception as e:
            logger.error(f"Error in Kafka consumer task: {e}")
        finally:
            if self.kafka_consumer:
                self.kafka_consumer.close()
    
    async def start_server(self):
        """Start the WebSocket server"""
        # Start Kafka consumer task
        kafka_task = asyncio.create_task(self.kafka_consumer_task())
        
        # Start WebSocket server
        server = await websockets.serve(
            self.handle_client,
            Config.WS_HOST,
            Config.WS_PORT
        )
        
        logger.info(f"WebSocket server started on ws://{Config.WS_HOST}:{Config.WS_PORT}")
        
        try:
            await server.wait_closed()
        except KeyboardInterrupt:
            logger.info("Shutting down WebSocket server...")
        finally:
            if self.kafka_consumer:
                self.kafka_consumer.close()
            server.close()
            await server.wait_closed()

async def main():
    """Main function to run the WebSocket server"""
    server = F1TelemetryWebSocketServer()
    await server.start_server()

if __name__ == "__main__":
    asyncio.run(main()) 