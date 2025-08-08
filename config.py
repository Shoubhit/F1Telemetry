import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Kafka Configuration
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_TOPIC_TELEMETRY = os.getenv('KAFKA_TOPIC_TELEMETRY', 'f1.telemetry')
    KAFKA_TOPIC_CONTROL = os.getenv('KAFKA_TOPIC_CONTROL', 'f1.control')

    # Azure Cosmos DB Configuration
    COSMOS_ENDPOINT = os.getenv('COSMOS_ENDPOINT')
    COSMOS_KEY = os.getenv('COSMOS_KEY')
    COSMOS_DATABASE = os.getenv('COSMOS_DATABASE', 'f1telemetry')
    COSMOS_CONTAINER = os.getenv('COSMOS_CONTAINER', 'telemetry')

    # Redis Configuration
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))

    # Simulation Configuration
    DEFAULT_PLAYBACK_SPEED = float(os.getenv('DEFAULT_PLAYBACK_SPEED', 1.0))
    DEFAULT_YEAR = int(os.getenv('DEFAULT_YEAR', 2023))
    DEFAULT_GRAND_PRIX = os.getenv('DEFAULT_GRAND_PRIX', 'Monza')
    DEFAULT_SESSION = os.getenv('DEFAULT_SESSION', 'R')
    DEFAULT_DRIVER = os.getenv('DEFAULT_DRIVER', 'VER')

    # WebSocket Configuration
    WS_HOST = os.getenv('WS_HOST', 'localhost')
    WS_PORT = int(os.getenv('WS_PORT', 8765))

    # API Configuration
    API_HOST = os.getenv('API_HOST', 'localhost')
    API_PORT = int(os.getenv('API_PORT', 8000)) 