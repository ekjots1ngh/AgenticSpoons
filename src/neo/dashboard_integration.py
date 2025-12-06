"""
AgentSpoons Dashboard + Neo Blockchain Integration
Bridges the Dash dashboard with Neo N3 smart contract
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Optional, List
from loguru import logger

from .blockchain_client import NeoBlockchainClient, VolatilityOracle
from .volatility_contract import display_contract


class DashboardNeoIntegration:
    """Bridge between Dash dashboard and Neo blockchain"""
    
    def __init__(self, network: str = "testnet", auto_submit: bool = True):
        """Initialize integration
        
        Args:
            network: 'testnet' or 'mainnet'
            auto_submit: Automatically submit volatility updates to blockchain
        """
        self.network = network
        self.auto_submit = auto_submit
        
        # Initialize Neo components
        self.client = NeoBlockchainClient(network=network)
        self.oracle = VolatilityOracle(network=network)
        
        # Tracking
        self.submission_history: List[Dict] = []
        self.submission_count = 0
        
        logger.info(f"Dashboard-Neo integration initialized (auto_submit={auto_submit})")
    
    def process_dashboard_data(self, data: Dict) -> Dict:
        """Process data from dashboard and prepare for blockchain
        
        Args:
            data: Dashboard data dict with volatility, pair, etc.
        
        Returns:
            Processed data ready for blockchain
        """
        try:
            pair = data.get('pair', 'NEO/USDT')
            realized_vol = data.get('realized_vol', 0.0)
            implied_vol = data.get('implied_vol', 0.0)
            garch_forecast = data.get('garch_forecast', 0.0)
            timestamp = data.get('timestamp', int(datetime.now().timestamp()))
            
            # Average the volatility measures for blockchain submission
            avg_vol = (realized_vol + implied_vol) / 2
            
            # Convert to basis points (0.45 -> 4500)
            vol_basis = int(avg_vol * 10000)
            
            processed = {
                'pair': pair,
                'volatility': avg_vol,
                'vol_basis': vol_basis,
                'realized_vol': realized_vol,
                'implied_vol': implied_vol,
                'garch_forecast': garch_forecast,
                'timestamp': timestamp,
                'ready_for_blockchain': True
            }
            
            return processed
            
        except Exception as e:
            logger.error(f"Failed to process dashboard data: {e}")
            return {'ready_for_blockchain': False, 'error': str(e)}
    
    def submit_to_blockchain(self, data: Dict) -> Optional[str]:
        """Submit volatility data to Neo blockchain
        
        Args:
            data: Processed data dict from process_dashboard_data()
        
        Returns:
            Transaction hash if successful, None otherwise
        """
        if not self.auto_submit:
            logger.debug("Auto-submit disabled")
            return None
        
        try:
            pair = data.get('pair', 'NEO/USDT')
            vol_basis = data.get('vol_basis', 0)
            timestamp = data.get('timestamp', int(datetime.now().timestamp()))
            
            # Submit to oracle
            success = self.oracle.submit_volatility(pair, vol_basis / 10000, timestamp)
            
            if success:
                self.submission_count += 1
                
                submission = {
                    'timestamp': datetime.now().isoformat(),
                    'pair': pair,
                    'volatility': vol_basis / 10000,
                    'blockchain_timestamp': timestamp,
                    'submission_id': self.submission_count
                }
                
                self.submission_history.append(submission)
                
                logger.success(f"Submitted to blockchain: {pair}={vol_basis/10000:.4f}")
                
                return f"0x{'a' * 64}"  # Mock transaction hash
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to submit to blockchain: {e}")
            return None
    
    def get_blockchain_status(self) -> Dict:
        """Get current blockchain status
        
        Returns:
            Dict with blockchain connection and contract status
        """
        try:
            net_info = self.client.get_network_info()
            contract_state = self.client.get_contract_state()
            cached_vols = self.oracle.get_all_volatilities()
            
            return {
                'network': self.network,
                'connected': bool(net_info),
                'network_info': net_info or {},
                'contract_deployed': self.client.contract_hash is not None,
                'contract_state': contract_state,
                'cached_volatilities': cached_vols,
                'total_submissions': self.submission_count,
                'submission_history_length': len(self.submission_history),
                'status': 'CONNECTED' if net_info else 'DISCONNECTED'
            }
            
        except Exception as e:
            logger.error(f"Failed to get blockchain status: {e}")
            return {
                'network': self.network,
                'status': 'ERROR',
                'error': str(e)
            }
    
    def get_wallet_info(self) -> Dict:
        """Get wallet information
        
        Returns:
            Dict with wallet address and balance
        """
        try:
            if not self.client.account:
                return {'status': 'no_wallet'}
            
            balance = self.client.get_balance()
            
            return {
                'address': self.client.account.address,
                'balance': balance,
                'network': self.network,
                'status': 'connected'
            }
            
        except Exception as e:
            logger.error(f"Failed to get wallet info: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def get_submission_history(self, limit: int = 10) -> List[Dict]:
        """Get recent blockchain submissions
        
        Args:
            limit: Number of recent submissions to return
        
        Returns:
            List of submission records
        """
        return self.submission_history[-limit:]
    
    def get_integration_metrics(self) -> Dict:
        """Get integration metrics for dashboard display
        
        Returns:
            Dict with key metrics
        """
        cached = self.oracle.get_all_volatilities()
        
        return {
            'blockchain_network': self.network,
            'auto_submit_enabled': self.auto_submit,
            'total_submissions': self.submission_count,
            'cached_pairs': len(cached),
            'submission_history_length': len(self.submission_history),
            'latest_submission': self.submission_history[-1] if self.submission_history else None,
            'blockchain_status': 'LIVE' if self.client.rpc_url else 'DISCONNECTED'
        }


class BlockchainDataStreamToDb:
    """Stream blockchain data to database for archival"""
    
    def __init__(self, integration: DashboardNeoIntegration, db_path: str = "data/blockchain_archive.json"):
        """Initialize archive
        
        Args:
            integration: DashboardNeoIntegration instance
            db_path: Path to archive JSON file
        """
        self.integration = integration
        self.db_path = db_path
        self.archive: List[Dict] = self._load_archive()
    
    def _load_archive(self) -> List[Dict]:
        """Load existing archive"""
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _save_archive(self):
        """Save archive to file"""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.archive, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save archive: {e}")
    
    def archive_submission(self, data: Dict):
        """Archive a blockchain submission
        
        Args:
            data: Submission data to archive
        """
        record = {
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'archive_index': len(self.archive)
        }
        
        self.archive.append(record)
        self._save_archive()
        
        logger.info(f"Archived submission #{len(self.archive)}")
    
    def get_archive_stats(self) -> Dict:
        """Get archive statistics
        
        Returns:
            Dict with archive stats
        """
        if not self.archive:
            return {'total_records': 0}
        
        total = len(self.archive)
        first_ts = self.archive[0].get('timestamp')
        last_ts = self.archive[-1].get('timestamp')
        
        # Count by pair
        pairs_count = {}
        for record in self.archive:
            pair = record.get('data', {}).get('pair', 'unknown')
            pairs_count[pair] = pairs_count.get(pair, 0) + 1
        
        return {
            'total_records': total,
            'first_timestamp': first_ts,
            'last_timestamp': last_ts,
            'pairs_tracked': len(pairs_count),
            'pairs_breakdown': pairs_count
        }


def demo_integration():
    """Demo the integration"""
    
    logger.info("=== AgentSpoons Dashboard + Neo Integration Demo ===")
    
    # Initialize integration
    integration = DashboardNeoIntegration(network="testnet", auto_submit=True)
    
    # Sample dashboard data
    dashboard_data = {
        'pair': 'NEO/USDT',
        'realized_vol': 0.45,
        'implied_vol': 0.48,
        'garch_forecast': 0.50,
        'timestamp': int(datetime.now().timestamp())
    }
    
    # Process data
    logger.info("Processing dashboard data...")
    processed = integration.process_dashboard_data(dashboard_data)
    logger.info(f"Processed: {processed}")
    
    # Submit to blockchain
    logger.info("Submitting to blockchain...")
    tx_hash = integration.submit_to_blockchain(processed)
    if tx_hash:
        logger.success(f"Transaction: {tx_hash}")
    
    # Get status
    logger.info("Blockchain status:")
    status = integration.get_blockchain_status()
    logger.info(f"  Network: {status.get('network')}")
    logger.info(f"  Status: {status.get('status')}")
    logger.info(f"  Submissions: {status.get('total_submissions')}")
    
    # Get metrics
    logger.info("Integration metrics:")
    metrics = integration.get_integration_metrics()
    for key, value in metrics.items():
        logger.info(f"  {key}: {value}")
    
    logger.success("Integration demo complete!")


if __name__ == "__main__":
    demo_integration()
