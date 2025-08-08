#!/usr/bin/env python3
"""
Simple test script to verify F1 Telemetry Pipeline setup
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_env_variables():
    """Test if environment variables are set correctly"""
    print("🔍 Checking environment variables...")
    
    required_vars = [
        'COSMOS_ENDPOINT',
        'COSMOS_KEY', 
        'COSMOS_DATABASE',
        'COSMOS_CONTAINER',
        'KAFKA_BOOTSTRAP_SERVERS'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * len(value) if 'KEY' in var else value}")
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        print("Please create a .env file with your configuration")
        return False
    
    return True

def test_cosmos_connection():
    """Test Cosmos DB connection"""
    print("\n🔍 Testing Cosmos DB connection...")
    
    try:
        from azure.cosmos import CosmosClient, PartitionKey
        from config import Config
        
        # Create client
        client = CosmosClient(Config.COSMOS_ENDPOINT, Config.COSMOS_KEY)
        
        # Test connection by listing databases
        databases = list(client.list_databases())
        print(f"✅ Cosmos DB connection successful! Found {len(databases)} databases")
        
        # Create database and container if they don't exist
        database = client.create_database_if_not_exists(Config.COSMOS_DATABASE)
        container = database.create_container_if_not_exists(
            id=Config.COSMOS_CONTAINER,
            partition_key=PartitionKey(path="/driver_id")
        )
        print(f"✅ Database '{Config.COSMOS_DATABASE}' and container '{Config.COSMOS_CONTAINER}' ready")
        
        return True
        
    except Exception as e:
        print(f"❌ Cosmos DB connection failed: {e}")
        return False

def test_kafka_connection():
    """Test Kafka connection"""
    print("\n🔍 Testing Kafka connection...")
    
    try:
        from kafka import KafkaProducer, KafkaConsumer
        from config import Config
        
        # Test producer
        producer = KafkaProducer(
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: v.encode('utf-8')
        )
        print("✅ Kafka producer connection successful")
        
        # Test consumer
        consumer = KafkaConsumer(
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='test-group'
        )
        print("✅ Kafka consumer connection successful")
        
        producer.close()
        consumer.close()
        return True
        
    except Exception as e:
        print(f"❌ Kafka connection failed: {e}")
        print("Make sure Kafka is running with: docker-compose up -d")
        return False

def main():
    """Main test function"""
    print("🏎️ F1 Telemetry Pipeline Setup Test")
    print("=" * 50)
    
    # Test environment variables
    if not test_env_variables():
        print("\n❌ Environment setup incomplete")
        return
    
    # Test Cosmos DB
    cosmos_ok = test_cosmos_connection()
    
    # Test Kafka
    kafka_ok = test_kafka_connection()
    
    print("\n" + "=" * 50)
    if cosmos_ok and kafka_ok:
        print("🎉 All tests passed! Your F1 Telemetry Pipeline is ready!")
        print("\nNext steps:")
        print("1. Start the pipeline: python start_pipeline.py")
        print("2. Access the dashboard: http://localhost:3000")
        print("3. Monitor Kafka: http://localhost:8080")
    else:
        print("❌ Some tests failed. Please check your configuration.")
        if not cosmos_ok:
            print("- Verify your Cosmos DB credentials in .env file")
        if not kafka_ok:
            print("- Start Kafka with: docker-compose up -d")

if __name__ == "__main__":
    main() 