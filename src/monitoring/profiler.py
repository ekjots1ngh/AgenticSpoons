"""
Performance profiling and monitoring
"""
import time
import functools
import psutil
import os
from loguru import logger
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Prometheus metrics
REQUEST_COUNT = Counter('agentspoons_requests_total', 'Total requests', ['endpoint'])
REQUEST_LATENCY = Histogram('agentspoons_request_duration_seconds', 'Request latency', ['endpoint'])
MEMORY_USAGE = Gauge('agentspoons_memory_bytes', 'Memory usage in bytes')
CPU_USAGE = Gauge('agentspoons_cpu_percent', 'CPU usage percentage')
VOLATILITY_CALCULATED = Counter('agentspoons_volatility_calculated_total', 'Volatility calculations', ['pair'])

def profile_function(func):
    """Decorator to profile function performance"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        
        duration = end_time - start_time
        memory_delta = end_memory - start_memory
        
        logger.info(f"{func.__name__}: {duration:.4f}s, Memory: {memory_delta:+.2f}MB")
        
        # Update Prometheus metrics
        REQUEST_COUNT.labels(endpoint=func.__name__).inc()
        REQUEST_LATENCY.labels(endpoint=func.__name__).observe(duration)
        
        return result
    
    return wrapper

class SystemMonitor:
    """Monitor system resources"""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
    
    def get_metrics(self):
        """Get current system metrics"""
        cpu_percent = self.process.cpu_percent(interval=1)
        memory_info = self.process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        
        # Update Prometheus gauges
        MEMORY_USAGE.set(memory_info.rss)
        CPU_USAGE.set(cpu_percent)
        
        return {
            'cpu_percent': cpu_percent,
            'memory_mb': memory_mb,
            'threads': self.process.num_threads(),
            'connections': len(self.process.connections())
        }
    
    def log_metrics(self):
        """Log current metrics"""
        metrics = self.get_metrics()
        logger.info(f"System: CPU={metrics['cpu_percent']:.1f}%, "
                   f"RAM={metrics['memory_mb']:.1f}MB, "
                   f"Threads={metrics['threads']}")

class PerformanceTracker:
    """Track performance over time"""
    
    def __init__(self):
        self.timings = {}
    
    def record(self, operation, duration):
        """Record operation timing"""
        if operation not in self.timings:
            self.timings[operation] = []
        
        self.timings[operation].append(duration)
    
    def get_stats(self, operation):
        """Get statistics for operation"""
        if operation not in self.timings:
            return None
        
        timings = self.timings[operation]
        
        return {
            'count': len(timings),
            'mean': sum(timings) / len(timings),
            'min': min(timings),
            'max': max(timings),
            'p50': sorted(timings)[len(timings)//2],
            'p95': sorted(timings)[int(len(timings)*0.95)],
            'p99': sorted(timings)[int(len(timings)*0.99)]
        }
    
    def print_report(self):
        """Print performance report"""
        print("\n" + "="*70)
        print("PERFORMANCE REPORT")
        print("="*70)
        
        for operation in sorted(self.timings.keys()):
            stats = self.get_stats(operation)
            print(f"\n{operation}:")
            print(f"  Count:  {stats['count']}")
            print(f"  Mean:   {stats['mean']*1000:.2f}ms")
            print(f"  P50:    {stats['p50']*1000:.2f}ms")
            print(f"  P95:    {stats['p95']*1000:.2f}ms")
            print(f"  P99:    {stats['p99']*1000:.2f}ms")

# Global instances
system_monitor = SystemMonitor()
performance_tracker = PerformanceTracker()

# Start Prometheus metrics server
def start_metrics_server(port=9090):
    """Start Prometheus metrics server"""
    start_http_server(port)
    logger.info(f"Metrics server started on port {port}")
