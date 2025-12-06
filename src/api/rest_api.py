"""
Professional REST API for AgentSpoons
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
import numpy as np
from loguru import logger

app = FastAPI(
    title="AgentSpoons API",
    description="Decentralized Volatility Oracle API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class VolatilityData(BaseModel):
    pair: str
    timestamp: str
    price: float
    realized_vol: float
    implied_vol: float
    garch_forecast: float
    spread: float

class HealthResponse(BaseModel):
    status: str
    agents_active: int
    last_update: str
    data_points: int

class ArbitrageSignal(BaseModel):
    timestamp: str
    pair: str
    spread: float
    direction: str  # "buy_iv" or "sell_iv"
    strength: float

# Helper function
def load_data():
    """Load volatility data from JSON"""
    try:
        with open('data/results.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return []

# Endpoints
@app.get("/", tags=["General"])
async def root():
    """API root - basic info and endpoints"""
    return {
        "name": "AgentSpoons API",
        "version": "1.0.0",
        "description": "Decentralized Volatility Oracle",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "health": "/health",
            "volatility": "/api/v1/volatility/{pair}",
            "latest": "/api/v1/latest",
            "arbitrage": "/api/v1/arbitrage",
            "history": "/api/v1/history/{pair}",
            "statistics": "/api/v1/stats/{pair}"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """System health check - returns operational status"""
    data = load_data()
    
    return HealthResponse(
        status="operational",
        agents_active=5,
        last_update=data[-1].get('timestamp', 'never') if data else "never",
        data_points=len(data)
    )

@app.get("/api/v1/volatility/{pair}", response_model=VolatilityData, tags=["Volatility"])
async def get_volatility(pair: str):
    """Get latest volatility data for a specific trading pair"""
    data = load_data()
    
    # Filter for pair
    pair_data = [d for d in data if d.get('pair') == pair]
    
    if not pair_data:
        raise HTTPException(status_code=404, detail=f"No data available for pair: {pair}")
    
    latest = pair_data[-1]
    return VolatilityData(
        pair=pair,
        timestamp=latest.get('timestamp', ''),
        price=float(latest.get('price', 0)),
        realized_vol=float(latest.get('realized_vol', 0)),
        implied_vol=float(latest.get('implied_vol', 0)),
        garch_forecast=float(latest.get('garch_forecast', 0)),
        spread=float(latest.get('spread', 0))
    )

@app.get("/api/v1/latest", response_model=List[dict], tags=["Volatility"])
async def get_latest(limit: int = Query(default=10, ge=1, le=100, description="Number of latest records")):
    """Get latest volatility data for all pairs"""
    data = load_data()
    return data[-limit:] if data else []

@app.get("/api/v1/arbitrage", tags=["Trading"])
async def get_arbitrage_signals(
    min_spread: float = Query(
        default=0.05,
        ge=0,
        le=1,
        description="Minimum spread threshold (0-1)"
    )
):
    """Get arbitrage opportunities where IV vs RV spread exceeds threshold"""
    data = load_data()
    
    # Filter for significant spreads
    opportunities = []
    for d in data:
        spread = float(d.get('spread', 0))
        if abs(spread) > min_spread:
            direction = "buy_iv" if spread < 0 else "sell_iv"
            strength = min(abs(spread) * 10, 1.0)  # Normalize to 0-1
            
            opportunities.append({
                "timestamp": d.get('timestamp'),
                "pair": d.get('pair'),
                "spread": spread,
                "direction": direction,
                "strength": strength
            })
    
    return {
        "threshold": min_spread,
        "opportunities_count": len(opportunities),
        "latest_signals": opportunities[-10:],  # Last 10
        "avg_spread": float(np.mean([abs(o['spread']) for o in opportunities])) if opportunities else 0.0,
        "best_signal": max(opportunities, key=lambda x: x['strength']) if opportunities else None
    }

@app.get("/api/v1/history/{pair}", tags=["Volatility"])
async def get_history(
    pair: str,
    limit: int = Query(default=100, ge=1, le=1000, description="Max records to return"),
    start: Optional[str] = Query(None, description="ISO timestamp start"),
    end: Optional[str] = Query(None, description="ISO timestamp end")
):
    """Get historical volatility data for a pair with optional date filtering"""
    data = load_data()
    
    # Filter for pair
    pair_data = [d for d in data if d.get('pair') == pair]
    
    # Filter by date if provided
    if start:
        pair_data = [d for d in pair_data if d.get('timestamp', '') >= start]
    if end:
        pair_data = [d for d in pair_data if d.get('timestamp', '') <= end]
    
    return {
        "pair": pair,
        "count": len(pair_data),
        "filters": {
            "limit": limit,
            "start": start,
            "end": end
        },
        "data": pair_data[-limit:]
    }

@app.get("/api/v1/stats/{pair}", tags=["Analytics"])
async def get_statistics(
    pair: str,
    window: int = Query(default=30, ge=1, le=365, description="Historical window in records")
):
    """Get statistical analysis of volatility - mean, std, min, max"""
    data = load_data()
    pair_data = [d for d in data if d.get('pair') == pair][-window:]
    
    if not pair_data:
        raise HTTPException(status_code=404, detail=f"Insufficient data for pair: {pair}")
    
    rvols = [float(d.get('realized_vol', 0)) for d in pair_data]
    ivols = [float(d.get('implied_vol', 0)) for d in pair_data]
    spreads = [float(d.get('spread', 0)) for d in pair_data]
    
    return {
        "pair": pair,
        "window": len(pair_data),
        "realized_vol": {
            "mean": float(np.mean(rvols)),
            "std": float(np.std(rvols)),
            "min": float(np.min(rvols)),
            "max": float(np.max(rvols)),
            "median": float(np.median(rvols))
        },
        "implied_vol": {
            "mean": float(np.mean(ivols)),
            "std": float(np.std(ivols)),
            "min": float(np.min(ivols)),
            "max": float(np.max(ivols)),
            "median": float(np.median(ivols))
        },
        "spread": {
            "mean": float(np.mean(spreads)),
            "std": float(np.std(spreads)),
            "min": float(np.min(spreads)),
            "max": float(np.max(spreads)),
            "median": float(np.median(spreads))
        }
    }

@app.get("/api/v1/pairs", tags=["Metadata"])
async def get_available_pairs():
    """Get all available trading pairs"""
    data = load_data()
    
    # Extract unique pairs
    pairs = list(set(d.get('pair') for d in data if 'pair' in d))
    
    return {
        "total_pairs": len(pairs),
        "pairs": sorted(pairs),
        "total_data_points": len(data),
        "last_update": data[-1].get('timestamp') if data else None
    }

@app.get("/api/v1/status", tags=["Monitoring"])
async def get_status():
    """Get detailed system status"""
    data = load_data()
    
    if not data:
        return {
            "status": "no_data",
            "data_points": 0,
            "uptime": "unknown"
        }
    
    # Get unique pairs
    pairs = list(set(d.get('pair') for d in data))
    
    # Calculate stats
    latest = data[-1]
    oldest = data[0]
    
    return {
        "status": "operational",
        "data_points": len(data),
        "pairs": len(pairs),
        "pair_list": sorted(pairs),
        "oldest_record": oldest.get('timestamp'),
        "latest_record": latest.get('timestamp'),
        "avg_realized_vol": float(np.mean([d.get('realized_vol', 0) for d in data])),
        "avg_implied_vol": float(np.mean([d.get('implied_vol', 0) for d in data])),
        "spread_median": float(np.median([d.get('spread', 0) for d in data]))
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*70)
    print(">> AgentSpoons REST API - Starting")
    print("="*70)
    print("API Docs:    http://localhost:8000/docs")
    print("ReDoc:       http://localhost:8000/redoc")
    print("OpenAPI:     http://localhost:8000/openapi.json")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
