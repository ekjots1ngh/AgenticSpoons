# AgenticSpoons Docker Deployment

This directory contains Docker configuration for containerizing the AgenticSpoons volatility analysis platform.

## 📦 Services

The Docker Compose setup includes 3 services:

1. **agentspoons-core** (port 8050, 8000, 8765)
   - Main data generator and processing engine
   - WebSocket server for real-time data
   - Core API endpoints

2. **agentspoons-dashboard** (port 8051)
   - Championship dashboard with live visualizations
   - Enhanced analytics interface
   - Statistical analysis tools

3. **agentspoons-api** (port 8001)
   - RESTful API server
   - Data query endpoints
   - Model status and predictions

## 🚀 Quick Start

### Build the images:
```bash
docker-compose build
```

### Run all services:
```bash
docker-compose up -d
```

### View logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f agentspoons-core
```

### Stop services:
```bash
docker-compose down
```

## 🌐 Access Points

Once running, access the services at:

- **Main Dashboard**: http://localhost:8050
- **Championship Dashboard**: http://localhost:8051
- **REST API**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8765

## 📂 Volumes

The following directories are mounted as volumes for data persistence:

- `./data` - Market data and JSON files
- `./logs` - Application logs
- `./wallets` - Neo N3 wallet files

## 🔧 Configuration

Environment variables in `docker-compose.yml`:

- `NEO_NETWORK`: Network for Neo N3 blockchain (testnet/mainnet)
- `LOG_LEVEL`: Logging verbosity (DEBUG/INFO/WARNING/ERROR)

## 🛠️ Development

### Rebuild after code changes:
```bash
docker-compose up -d --build
```

### Execute commands in container:
```bash
docker-compose exec agentspoons-core python showcase_complete_system.py
```

### Shell access:
```bash
docker-compose exec agentspoons-core /bin/bash
```

## 📊 Production Deployment

For production use:

1. Update environment variables in `docker-compose.yml`
2. Configure reverse proxy (nginx/traefik) for HTTPS
3. Set up monitoring and logging aggregation
4. Use Docker secrets for sensitive data
5. Enable automatic restarts: `restart: unless-stopped`

## 🐛 Troubleshooting

### Check container status:
```bash
docker-compose ps
```

### View resource usage:
```bash
docker stats
```

### Reset everything:
```bash
docker-compose down -v
docker-compose up -d --build
```

## 📋 Requirements

- Docker Engine 20.10+
- Docker Compose 1.29+
- 2GB+ available RAM
- 1GB+ disk space

## 🔒 Security Notes

- The containers run as non-root user
- No sensitive data in image layers
- Volume mounts for persistent data only
- Network isolation between services
- Use `.dockerignore` to exclude unnecessary files

## 📝 Image Details

- **Base Image**: python:3.10-slim
- **Size**: ~500MB (optimized with multi-stage build potential)
- **Dependencies**: All from requirements.txt
- **Ports**: 8050 (Dash), 8000 (API), 8765 (WebSocket)

## 🎯 Next Steps

1. Build images: `docker-compose build`
2. Start services: `docker-compose up -d`
3. Check logs: `docker-compose logs -f`
4. Access dashboard: http://localhost:8050
5. Test API: http://localhost:8000/docs

System is now fully containerized and ready for deployment! 🚀
