"""
Database Layer - SQLite for persistence
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
from loguru import logger
from pathlib import Path

class AgentSpoonsDB:
    """Database handler for AgentSpoons data"""
    
    def __init__(self, db_path: str = "data/agentspoons.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Initialize database schema"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Market data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                UNIQUE(pair, timestamp)
            )
        """)
        
        # Volatility metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS volatility_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                close_to_close_vol REAL,
                parkinson_vol REAL,
                garman_klass_vol REAL,
                rogers_satchell_vol REAL,
                yang_zhang_vol REAL,
                realized_vol_30d REAL,
                garch_forecast REAL,
                garch_omega REAL,
                garch_alpha REAL,
                garch_beta REAL,
                vol_regime TEXT,
                UNIQUE(pair, timestamp)
            )
        """)
        
        # Implied volatility table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS implied_volatility (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                spot_price REAL,
                atm_vol_1w REAL,
                atm_vol_1m REAL,
                atm_vol_3m REAL,
                atm_vol_6m REAL,
                vol_skew_30d REAL,
                smile_curvature_30d REAL,
                UNIQUE(pair, timestamp)
            )
        """)
        
        # Arbitrage opportunities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS arbitrage_opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                spot_price REAL,
                realized_vol REAL,
                implied_vol REAL,
                garch_forecast REAL,
                vol_spread REAL,
                vol_spread_pct REAL,
                strategy TEXT,
                direction TEXT,
                confidence REAL,
                reasoning TEXT,
                recommended_action TEXT
            )
        """)
        
        # Oracle publications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS oracle_publications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                tx_hash TEXT,
                block_height INTEGER,
                gas_cost REAL,
                oracle_data JSON,
                status TEXT
            )
        """)
        
        # Greeks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS greeks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                strike REAL,
                maturity REAL,
                option_type TEXT,
                spot REAL,
                sigma REAL,
                delta REAL,
                gamma REAL,
                vega REAL,
                theta REAL,
                rho REAL,
                price REAL
            )
        """)
        
        self.conn.commit()
        logger.info(f"Database initialized at {self.db_path}")
    
    def insert_market_data(self, pair: str, data: Dict):
        """Insert market data point"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO market_data 
            (pair, timestamp, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pair,
            data['timestamp'],
            data['open'],
            data['high'],
            data['low'],
            data['close'],
            data['volume']
        ))
        self.conn.commit()
    
    def insert_volatility_metrics(self, pair: str, metrics: Dict):
        """Insert volatility calculation results"""
        cursor = self.conn.cursor()
        garch_params = metrics.get('garch_params', {})
        
        cursor.execute("""
            INSERT OR REPLACE INTO volatility_metrics
            (pair, timestamp, close_to_close_vol, parkinson_vol, garman_klass_vol,
             rogers_satchell_vol, yang_zhang_vol, realized_vol_30d, garch_forecast,
             garch_omega, garch_alpha, garch_beta, vol_regime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pair,
            metrics['timestamp'],
            metrics.get('close_to_close_vol'),
            metrics.get('parkinson_vol'),
            metrics.get('garman_klass_vol'),
            metrics.get('rogers_satchell_vol'),
            metrics.get('yang_zhang_vol'),
            metrics.get('realized_vol_30d'),
            metrics.get('garch_forecast'),
            garch_params.get('omega'),
            garch_params.get('alpha'),
            garch_params.get('beta'),
            metrics.get('vol_regime')
        ))
        self.conn.commit()
    
    def insert_implied_vol(self, pair: str, iv_data: Dict):
        """Insert implied volatility data"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO implied_volatility
            (pair, timestamp, spot_price, atm_vol_1w, atm_vol_1m, atm_vol_3m,
             atm_vol_6m, vol_skew_30d, smile_curvature_30d)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pair,
            datetime.now().isoformat(),
            iv_data.get('spot_price'),
            iv_data.get('atm_vol_1w'),
            iv_data.get('atm_vol_1m'),
            iv_data.get('atm_vol_3m'),
            iv_data.get('atm_vol_6m'),
            iv_data.get('vol_skew_30d'),
            iv_data.get('smile_curvature_30d')
        ))
        self.conn.commit()
    
    def insert_arbitrage_opportunity(self, opportunity: Dict):
        """Insert arbitrage opportunity"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO arbitrage_opportunities
            (pair, timestamp, spot_price, realized_vol, implied_vol, garch_forecast,
             vol_spread, vol_spread_pct, strategy, direction, confidence, reasoning,
             recommended_action)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            opportunity['pair'],
            opportunity['timestamp'],
            opportunity['spot_price'],
            opportunity['realized_vol'],
            opportunity['implied_vol'],
            opportunity['garch_forecast'],
            opportunity['vol_spread'],
            opportunity['vol_spread_pct'],
            opportunity['strategy'],
            opportunity['direction'],
            opportunity['confidence'],
            opportunity['reasoning'],
            opportunity['recommended_action']
        ))
        self.conn.commit()
    
    def insert_oracle_publication(self, pair: str, oracle_data: Dict, tx_hash: str = ""):
        """Record oracle publication"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO oracle_publications
            (pair, timestamp, tx_hash, oracle_data, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            pair,
            datetime.now().isoformat(),
            tx_hash,
            json.dumps(oracle_data),
            'published' if tx_hash else 'pending'
        ))
        self.conn.commit()
    
    def get_recent_volatility(self, pair: str, limit: int = 100) -> List[Dict]:
        """Get recent volatility metrics"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM volatility_metrics
            WHERE pair = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (pair, limit))
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_arbitrage_opportunities(self, hours: int = 24) -> List[Dict]:
        """Get recent arbitrage opportunities"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM arbitrage_opportunities
            WHERE timestamp > datetime('now', '-' || ? || ' hours')
            ORDER BY confidence DESC
        """, (hours,))
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_volatility_timeseries(self, pair: str, days: int = 7) -> Dict:
        """Get volatility time series for charting"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT timestamp, garman_klass_vol, garch_forecast
            FROM volatility_metrics
            WHERE pair = ? AND timestamp > datetime('now', '-' || ? || ' days')
            ORDER BY timestamp ASC
        """, (pair, days))
        
        data = cursor.fetchall()
        return {
            'timestamps': [row[0] for row in data],
            'realized_vol': [row[1] for row in data],
            'garch_forecast': [row[2] for row in data]
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
