"""
Professional Backtesting Framework
"""
import backtrader as bt
import numpy as np
import pandas as pd
from datetime import datetime
import json

class VolatilityArbitrageStrategy(bt.Strategy):
    """Volatility arbitrage strategy"""
    
    params = (
        ('spread_threshold', 0.10),
        ('position_size', 0.95),
        ('stop_loss', 0.05),
        ('take_profit', 0.15),
    )
    
    def __init__(self):
        # Custom data feeds for volatility
        self.realized_vol = self.datas[0].realized_vol
        self.implied_vol = self.datas[0].implied_vol
        
        # Indicators
        self.spread = self.implied_vol - self.realized_vol
        self.spread_ma = bt.indicators.SMA(self.spread, period=20)
        self.spread_std = bt.indicators.StdDev(self.spread, period=20)
        
        # Track orders
        self.order = None
        self.entry_price = None
        self.entry_spread = None
    
    def log(self, txt, dt=None):
        """Logging function"""
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')
    
    def notify_order(self, order):
        """Order notifications"""
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}')
            
            self.entry_price = order.executed.price
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        
        self.order = None
    
    def notify_trade(self, trade):
        """Trade notifications"""
        if not trade.isclosed:
            return
        
        self.log(f'TRADE PROFIT, GROSS: {trade.pnl:.2f}, NET: {trade.pnlcomm:.2f}')
    
    def next(self):
        """Strategy logic"""
        # Skip if order pending
        if self.order:
            return
        
        current_spread = self.spread[0]
        rv = self.realized_vol[0]
        iv = self.implied_vol[0]
        
        # Not in position
        if not self.position:
            # Sell volatility (short straddle) if IV > RV significantly
            if current_spread > self.params.spread_threshold:
                size = int(self.broker.getvalue() * self.params.position_size / self.data.close[0])
                self.order = self.sell(size=size)
                self.entry_spread = current_spread
                self.log(f'SELL SIGNAL, Spread: {current_spread:.4f}')
            
            # Buy volatility (long straddle) if RV > IV significantly
            elif current_spread < -self.params.spread_threshold:
                size = int(self.broker.getvalue() * self.params.position_size / self.data.close[0])
                self.order = self.buy(size=size)
                self.entry_spread = current_spread
                self.log(f'BUY SIGNAL, Spread: {current_spread:.4f}')
        
        # In position - check exit conditions
        else:
            pnl_pct = (self.data.close[0] - self.entry_price) / self.entry_price
            
            # Stop loss
            if abs(pnl_pct) > self.params.stop_loss:
                self.order = self.close()
                self.log(f'STOP LOSS, PnL: {pnl_pct:.2%}')
            
            # Take profit
            elif abs(pnl_pct) > self.params.take_profit:
                self.order = self.close()
                self.log(f'TAKE PROFIT, PnL: {pnl_pct:.2%}')
            
            # Mean reversion - close if spread normalizes
            elif abs(current_spread) < 0.03:
                self.order = self.close()
                self.log(f'SPREAD NORMALIZED, Closing')

class GARCHMomentumStrategy(bt.Strategy):
    """Trade based on GARCH forecasts"""
    
    params = (
        ('forecast_threshold', 0.15),
        ('lookback', 50),
    )
    
    def __init__(self):
        self.garch_forecast = self.datas[0].garch_forecast
        self.realized_vol = self.datas[0].realized_vol
        
        # Moving averages
        self.vol_ma_short = bt.indicators.SMA(self.realized_vol, period=10)
        self.vol_ma_long = bt.indicators.SMA(self.realized_vol, period=50)
        
        self.order = None
    
    def next(self):
        """Strategy logic"""
        if self.order:
            return
        
        forecast = self.garch_forecast[0]
        current_vol = self.realized_vol[0]
        
        # Volatility regime detection
        vol_increasing = self.vol_ma_short[0] > self.vol_ma_long[0]
        forecast_spike = forecast > current_vol * 1.2
        
        if not self.position:
            # Buy if expecting volatility spike
            if vol_increasing and forecast_spike:
                self.order = self.buy()
        
        else:
            # Sell if volatility peaked
            if not vol_increasing:
                self.order = self.close()

class CustomDataFeed(bt.feeds.PandasData):
    """Custom data feed with volatility fields"""
    
    lines = ('realized_vol', 'implied_vol', 'garch_forecast')
    
    params = (
        ('datetime', None),
        ('open', 'price'),
        ('high', 'price'),
        ('low', 'price'),
        ('close', 'price'),
        ('volume', -1),
        ('openinterest', -1),
        ('realized_vol', 'realized_vol'),
        ('implied_vol', 'implied_vol'),
        ('garch_forecast', 'garch_forecast'),
    )

class BacktestEngine:
    """Main backtesting engine"""
    
    def __init__(self, initial_cash=100000):
        self.cerebro = bt.Cerebro()
        self.cerebro.broker.setcash(initial_cash)
        self.cerebro.broker.setcommission(commission=0.001)  # 0.1%
        
        # Add analyzers
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    
    def load_data(self, data_file='data/results.json'):
        """Load data from JSON"""
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        neo_data = [d for d in data if d['pair'] == 'NEO/USDT']
        
        # Convert to DataFrame
        df = pd.DataFrame(neo_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        # Ensure all required fields
        df['high'] = df['price'] * 1.01
        df['low'] = df['price'] * 0.99
        df['volume'] = 0
        
        return df
    
    def add_strategy(self, strategy_class, **params):
        """Add strategy with parameters"""
        self.cerebro.addstrategy(strategy_class, **params)
    
    def run(self, data):
        """Run backtest"""
        # Add data feed
        data_feed = CustomDataFeed(dataname=data)
        self.cerebro.adddata(data_feed)
        
        # Print starting conditions
        print('='*70)
        print('BACKTEST RESULTS')
        print('='*70)
        print(f'Starting Portfolio Value: ${self.cerebro.broker.getvalue():,.2f}')
        
        # Run backtest
        results = self.cerebro.run()
        strat = results[0]
        
        # Print final conditions
        print(f'Final Portfolio Value: ${self.cerebro.broker.getvalue():,.2f}')
        
        # Extract analytics
        sharpe = strat.analyzers.sharpe.get_analysis()
        drawdown = strat.analyzers.drawdown.get_analysis()
        returns = strat.analyzers.returns.get_analysis()
        trades = strat.analyzers.trades.get_analysis()
        
        print(f'\nPerformance Metrics:')
        sharpe_ratio = sharpe.get("sharperatio", None)
        print(f'  Sharpe Ratio:     {sharpe_ratio:.2f}' if sharpe_ratio else '  Sharpe Ratio:     N/A')
        print(f'  Max Drawdown:     {drawdown.max.drawdown:.2%}')
        
        total_return = returns.get('rtot', None)
        print(f'  Total Return:     {total_return:.2%}' if total_return else '  Total Return:     N/A')
        
        if 'total' in trades and trades.total.total > 0:
            print(f'  Total Trades:     {trades.total.total}')
            print(f'  Win Rate:         {trades.won.total / trades.total.total:.2%}')
        else:
            print(f'  Total Trades:     0')
            print(f'  Win Rate:         N/A')
        
        print('='*70)
        
        return strat
    
    def plot(self):
        """Plot backtest results"""
        self.cerebro.plot(style='candlestick')

# ========== OPTIMIZATION ==========
class StrategyOptimizer:
    """Optimize strategy parameters"""
    
    def __init__(self, data):
        self.data = data
    
    def optimize(self, strategy_class, param_grid):
        """Grid search optimization"""
        best_sharpe = -float('inf')
        best_params = None
        results = []
        
        print("Running optimization...")
        
        for params in self._generate_params(param_grid):
            cerebro = bt.Cerebro()
            cerebro.broker.setcash(100000)
            cerebro.broker.setcommission(commission=0.001)
            
            data_feed = CustomDataFeed(dataname=self.data)
            cerebro.adddata(data_feed)
            
            cerebro.addstrategy(strategy_class, **params)
            cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
            
            strat = cerebro.run()[0]
            sharpe = strat.analyzers.sharpe.get_analysis().get('sharperatio', 0)
            
            if sharpe and sharpe > best_sharpe:
                best_sharpe = sharpe
                best_params = params
            
            results.append({
                'params': params,
                'sharpe': sharpe,
                'final_value': cerebro.broker.getvalue()
            })
        
        print(f"\nBest parameters: {best_params}")
        print(f"Best Sharpe: {best_sharpe:.2f}")
        
        return best_params, results
    
    def _generate_params(self, param_grid):
        """Generate parameter combinations"""
        import itertools
        
        keys = param_grid.keys()
        values = param_grid.values()
        
        for combination in itertools.product(*values):
            yield dict(zip(keys, combination))

# ========== MAIN SCRIPT ==========
def run_backtest():
    """Run complete backtest"""
    
    # Initialize engine
    engine = BacktestEngine(initial_cash=100000)
    
    # Load data
    data = engine.load_data()
    
    if len(data) < 100:
        print("Need more data for backtesting")
        return
    
    # Add strategy
    engine.add_strategy(
        VolatilityArbitrageStrategy,
        spread_threshold=0.08,
        position_size=0.90
    )
    
    # Run
    engine.run(data)
    
    # Plot
    # engine.plot()

def run_optimization():
    """Run parameter optimization"""
    
    engine = BacktestEngine()
    data = engine.load_data()
    
    optimizer = StrategyOptimizer(data)
    
    param_grid = {
        'spread_threshold': [0.05, 0.08, 0.10, 0.12],
        'position_size': [0.80, 0.90, 0.95],
        'stop_loss': [0.03, 0.05, 0.07],
    }
    
    best_params, results = optimizer.optimize(
        VolatilityArbitrageStrategy,
        param_grid
    )
    
    # Save results
    pd.DataFrame(results).to_csv('data/optimization_results.csv', index=False)
    print("\n✅ Results saved to data/optimization_results.csv")

if __name__ == "__main__":
    print("Choose mode:")
    print("1. Run backtest")
    print("2. Run optimization")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == '1':
        run_backtest()
    elif choice == '2':
        run_optimization()
    else:
        print("Invalid choice")
