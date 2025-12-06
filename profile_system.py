"""
Profile the entire system
"""
import cProfile
import pstats
from pstats import SortKey
import io

def profile_enhanced_demo():
    """Profile the data generation system"""
    import sys
    sys.path.insert(0, 'src')
    
    from enhanced_demo import AdvancedDataGenerator
    import asyncio
    
    async def run_cycles():
        gen = AdvancedDataGenerator()
        for _ in range(100):
            await gen.run()
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    asyncio.run(run_cycles())
    
    profiler.disable()
    
    # Print stats
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats(SortKey.CUMULATIVE)
    ps.print_stats(20)
    
    print(s.getvalue())
    
    # Save to file
    ps.dump_stats('data/profile_stats.prof')
    print("\n✅ Profile saved to data/profile_stats.prof")
    print("   View with: snakeviz data/profile_stats.prof")

if __name__ == "__main__":
    profile_enhanced_demo()
