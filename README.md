# 🏎️ F1 Telemetry Simulation Pipeline

A real-time F1 telemetry simulation pipeline using Apache Kafka, Azure Cosmos DB, and Next.js frontend.

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Set up Environment Variables**
```bash
# Copy the example file
cp env.example .env

# Edit .env with your Cosmos DB credentials
# Get these from Azure Portal > Your Cosmos DB Account > Keys
```

### 3. **Start Kafka**
```bash
docker-compose up -d
```

### 4. **Test the Setup**
```bash
python test_setup.py
```

### 5. **Run the Pipeline**
```bash
python start_pipeline.py
```

## 📋 Prerequisites

- **Python 3.8+**
- **Docker Desktop** (for Kafka)
- **Azure Cosmos DB Account** (already set up)
- **Node.js** (for frontend, optional)

## 🔧 Configuration

### Environment Variables (.env file)
```
# Azure Cosmos DB
COSMOS_ENDPOINT=https://your-account.documents.azure.com:443/
COSMOS_KEY=your-primary-key

# Kafka (defaults work for local setup)
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# Simulation Settings
DEFAULT_YEAR=2023
DEFAULT_GRAND_PRIX=Monza
DEFAULT_DRIVER=VER
```

## 🏁 Running the Pipeline

### Option 1: Simple Test
```bash
python test_setup.py
```

### Option 2: Full Pipeline (when all files are recreated)
```bash
python start_pipeline.py
```

## 📊 Monitoring

- **Kafka UI**: http://localhost:8080
- **Frontend Dashboard**: http://localhost:3000 (when recreated)
- **API Server**: http://localhost:8000 (when recreated)

## 🛠️ Troubleshooting

### Kafka Issues
```bash
# Check if Kafka is running
docker-compose ps

# Restart Kafka
docker-compose restart

# View logs
docker-compose logs kafka
```

### Cosmos DB Issues
- Verify your `.env` file has correct credentials
- Check Azure Portal for your Cosmos DB endpoint and key
- Ensure your Cosmos DB account is running

### Python Dependencies
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📁 Project Structure

```
F1Telemetry/
├── config.py              # Configuration management
├── models.py              # Pydantic data models
├── test_setup.py          # Setup verification
├── docker-compose.yml     # Kafka setup
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from env.example)
└── README.md             # This file
```

## 🎯 What's Working

✅ **Azure Cosmos DB**: Connected and ready  
✅ **Apache Kafka**: Running locally with Docker  
✅ **Python Dependencies**: All installed  
✅ **Configuration**: Environment-based setup  
✅ **Testing**: Verification script available  

## 🚧 Next Steps

The core infrastructure is ready! The following files need to be recreated for the full pipeline:
- `telemetry_extractor.py` - FastF1 data extraction
- `kafka_producer.py` - Kafka message producer
- `kafka_consumer.py` - Kafka message consumer
- `websocket_server.py` - Real-time WebSocket server
- `api_server.py` - FastAPI backend
- `start_pipeline.py` - Main orchestration script
- Frontend files (Next.js components)

## 📞 Support

If you encounter issues:
1. Run `python test_setup.py` to verify your setup
2. Check the troubleshooting section above
3. Ensure Docker Desktop is running for Kafka
4. Verify your Cosmos DB credentials in `.env` 