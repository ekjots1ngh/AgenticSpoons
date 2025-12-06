"""
Python bridge to OCaml volatility engine
Provides high-performance numerical computation
"""
import json
import subprocess
from typing import Dict, List, Any
from loguru import logger
from pathlib import Path

class OCamlVolatilityEngine:
    """Interface to OCaml high-performance engine"""
    
    def __init__(self):
        self.ocaml_binary = Path("../ocaml-engine/_build/default/bin/vol_server.exe")
        self.process = None
        
        if not self.ocaml_binary.exists():
            logger.warning("OCaml engine not found. Install with: cd ocaml-engine && dune build")
            self.enabled = False
        else:
            self.enabled = True
            logger.info("✓ OCaml engine available for high-performance computation")
    
    def _call_ocaml(self, method: str, params: Dict) -> Dict:
        """Call OCaml engine via JSON-RPC"""
        if not self.enabled:
            raise RuntimeError("OCaml engine not available")
        
        request = json.dumps({"method": method, "params": params})
        
        try:
            result = subprocess.run(
                [str(self.ocaml_binary)],
                input=request,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"OCaml engine error: {result.stderr}")
            
            return json.loads(result.stdout.strip())
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("OCaml engine timeout")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON from OCaml: {e}")
    
    def calculate_volatility(self, ohlcv_data: List[Dict]) -> Dict[str, float]:
        """
        Calculate all volatility metrics using OCaml
        
        Args:
            ohlcv_data: List of {"timestamp", "open", "high", "low", "close", "volume"}
        
        Returns:
            Dict with all volatility estimators
        """
        params = {"data": ohlcv_data}
        return self._call_ocaml("calculate_volatility", params)
    
    def calculate_greeks(self, spot: float, strike: float, maturity: float,
                        risk_free_rate: float, volatility: float,
                        option_type: str = "call") -> Dict[str, float]:
        """
        Calculate option Greeks using OCaml
        
        Returns:
            {"delta", "gamma", "vega", "theta", "rho"}
        """
        params = {
            "spot": spot,
            "strike": strike,
            "maturity": maturity,
            "risk_free_rate": risk_free_rate,
            "volatility": volatility,
            "option_type": option_type
        }
        return self._call_ocaml("calculate_greeks", params)
    
    def fit_garch(self, returns: List[float]) -> Dict:
        """
        Fit GARCH(1,1) model using OCaml
        
        Returns:
            {"params": {"omega", "alpha", "beta"}, "conditional_variance": [...], "log_likelihood": ...}
        """
        params = {"returns": returns}
        return self._call_ocaml("fit_garch", params)
    
    def monte_carlo_option(self, spot: float, strike: float, maturity: float,
                          risk_free_rate: float, volatility: float,
                          option_type: str = "call", n_paths: int = 10000) -> Dict:
        """
        Price option using Monte Carlo simulation in OCaml
        
        Returns:
            {"price": ..., "std_error": ...}
        """
        params = {
            "spot": spot,
            "strike": strike,
            "maturity": maturity,
            "risk_free_rate": risk_free_rate,
            "volatility": volatility,
            "option_type": option_type,
            "n_paths": n_paths
        }
        return self._call_ocaml("monte_carlo_option", params)

# Global instance
ocaml_engine = OCamlVolatilityEngine()
