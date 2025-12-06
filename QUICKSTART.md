# 🚀 AgentSpoons Quick Start Guide

## One-Command Demo

Run the complete system demonstration with all features:

### Windows
```powershell
.\run_complete_demo.ps1
```

### Linux/Mac
```bash
./run_complete_demo.sh
```

This will:
1. ✅ Generate impressive demo data (200+ data points)
2. ✅ Train ML volatility prediction model (XGBoost)
3. ✅ Run backtesting engine
4. ✅ Generate professional PDF report
5. ✅ Create 3D volatility surface visualization
6. ✅ Setup Neo N3 wallet
7. ✅ Start all services (Dashboard, API, WebSocket)
8. ✅ Test API endpoints

## Individual Commands

### Generate Data
```bash
python src/enhanced_demo.py
```

### Train ML Model
```bash
python src/ml/volatility_predictor.py
```

### Generate PDF Report
```bash
python src/reports/pdf_generator.py
```

### Create 3D Surface
```bash
python -c "from src.visualization.vol_surface_3d import VolatilitySurface3D; import plotly.offline as pyo; surf = VolatilitySurface3D(); fig = surf.generate_sample_surface(); pyo.plot(fig, filename='data/vol_surface.html')"
```

### Start Full System
```bash
# Windows
.\run_full_system.ps1

# Linux/Mac
./run_full_system.sh
```

### Test API
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/volatility/NEO-USDT
```

### Stop All Services
```bash
# Windows
.\stop_system.ps1

# Linux/Mac
./stop_system.sh
```

## Access Points

Once running:

- **Dashboard**: http://localhost:8050
- **API Documentation**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8765

## Generated Assets

After running the demo:

- `data/results.json` - Market data with volatility metrics
- `models/ml_vol_predictor.pkl` - Trained ML model (18KB)
- `reports/volatility_report_*.pdf` - Professional PDF report (25KB)
- `data/vol_surface.html` - Interactive 3D surface (4.6MB)
- `data/vol_surface_3d.html` - Full 3D visualization
- `data/vol_smile.html` - Volatility smile chart
- `data/term_structure.html` - Term structure chart

## View Logs

**Windows:**
```powershell
Get-Content logs/data_generator.log -Wait
Get-Content logs/dashboard.log -Wait
Get-Content logs/api.log -Wait
```

**Linux/Mac:**
```bash
tail -f logs/data_generator.log
tail -f logs/dashboard.log
tail -f logs/api.log
```

## Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Troubleshooting

**Services won't start:**
```bash
# Kill any existing processes
# Windows
Stop-Process -Name python -Force

# Linux/Mac
pkill -f python
```

**Missing data:**
```bash
# Regenerate demo data
python src/enhanced_demo.py
```

**API returns 404:**
```bash
# Check if API is running
curl http://localhost:8000/health

# Restart API
python src/api/rest_api.py
```

## System Requirements

- Python 3.10+
- 2GB RAM minimum
- 1GB disk space
- Neo N3 RPC access (optional)

## Next Steps

1. **Explore Dashboard**: http://localhost:8050
2. **Read API Docs**: http://localhost:8000/docs
3. **View PDF Report**: Open `reports/volatility_report_*.pdf`
4. **Check 3D Surface**: Open `data/vol_surface.html` in browser
5. **Review Code**: Read `COMPLETE_DOCUMENTATION.md`

---

**Built for Neo Blockchain Hackathon 2025** 🥄✨
