"""
AgentSpoons Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Neo Blockchain
    NEO_RPC_URL = os.getenv("NEO_RPC_URL", "https://testnet1.neo.coz.io:443")
    NEO_NETWORK = os.getenv("NEO_NETWORK", "testnet")
    
    # Wallet Configuration
    WALLET_PATH = os.getenv("WALLET_PATH", "./wallet.json")
    WALLET_PASSWORD = os.getenv("WALLET_PASSWORD", "")
    
    # Agent Configuration
    DATA_COLLECTION_INTERVAL = int(os.getenv("DATA_COLLECTION_INTERVAL", "30"))
    VOL_CALCULATION_INTERVAL = int(os.getenv("VOL_CALCULATION_INTERVAL", "60"))
    IV_CALCULATION_INTERVAL = int(os.getenv("IV_CALCULATION_INTERVAL", "120"))
    
    # Market Data
    TOKEN_PAIRS = ["NEO/USDT", "GAS/USDT"]
    DEX_ENDPOINTS = [
        "https://api.flamingo.finance",  # Example
        # Add more DEX endpoints
    ]
    
    # Risk Parameters
    RISK_FREE_RATE = float(os.getenv("RISK_FREE_RATE", "0.05"))
    
    # Database
    DATA_DIR = "./data"
    DB_PATH = os.path.join(DATA_DIR, "agentspoons.db")
    
    # Dashboard
    DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "127.0.0.1")
    DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8050"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

config = Config()
