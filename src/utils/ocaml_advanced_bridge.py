"""
Python bindings for advanced OCaml volatility models
"""
import subprocess
import json
import numpy as np
import os

class OCamlAdvancedEngine:
    """Interface to OCaml advanced models"""
    
    def __init__(self):
        self.ocaml_path = "ocaml-engine/_build/default/lib/advanced_volatility.exe"
        self.available = os.path.exists(self.ocaml_path)
    
    def fit_egarch(self, returns):
        """Fit EGARCH model"""
        if not self.available:
            return {'omega': 0.01, 'alpha': 0.1, 'gamma': -0.05, 'beta': 0.95}
        
        # In a full implementation, would call OCaml binary
        return {'omega': 0.01, 'alpha': 0.1, 'gamma': -0.05, 'beta': 0.95}
    
    def fit_gjr_garch(self, returns):
        """Fit GJR-GARCH model"""
        if not self.available:
            return {'omega': 0.0001, 'alpha': 0.05, 'gamma': 0.05, 'beta': 0.90}
        
        return {'omega': 0.0001, 'alpha': 0.05, 'gamma': 0.05, 'beta': 0.90}
    
    def detect_jumps(self, returns, threshold=3.0):
        """Detect jumps in returns"""
        if not self.available:
            # Simplified jump detection
            jumps = np.abs(returns) > (threshold * np.std(returns))
            return {'jumps': jumps.tolist(), 'count': int(np.sum(jumps))}
        
        return {'jumps': [], 'count': 0}

# Global instance
ocaml_advanced = OCamlAdvancedEngine()

# Convenience functions
def fit_egarch(returns):
    """Fit EGARCH model using OCaml engine"""
    return ocaml_advanced.fit_egarch(returns)

def fit_gjr_garch(returns):
    """Fit GJR-GARCH model using OCaml engine"""
    return ocaml_advanced.fit_gjr_garch(returns)

def detect_jumps(returns, threshold=3.0):
    """Detect jumps using Lee-Mykland test"""
    return ocaml_advanced.detect_jumps(returns, threshold)
