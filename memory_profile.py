"""
Memory profiling
"""
from memory_profiler import profile
import numpy as np

@profile
def memory_intensive_calculation():
    """Test memory usage"""
    # Simulate large calculations
    data = []
    
    for i in range(1000):
        arr = np.random.randn(1000, 100)
        result = np.dot(arr, arr.T)
        data.append(result)
    
    return data

if __name__ == "__main__":
    print("Running memory profile...")
    memory_intensive_calculation()
