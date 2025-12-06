# Advanced Time Series Forecasting

Professional-grade time series forecasting for volatility prediction using ARIMA, Prophet, and ensemble methods.

## 📊 Models Implemented

### 1. ARIMA (AutoRegressive Integrated Moving Average)
**Best for:** Short-term trends, stationary series

```python
from src.forecasting.time_series_models import ARIMAForecaster

arima = ARIMAForecaster()

# Auto-tune parameters
arima.auto_arima(volatility_data)  # Finds best (p,d,q)

# Fit model
arima.fit(volatility_data)

# Forecast 10 steps ahead
forecast = arima.forecast(steps=10)
print(forecast['forecast'])
print(f"Confidence: [{forecast['lower_bound']}, {forecast['upper_bound']}]")
```

**Features:**
- Automatic parameter selection via `pmdarima`
- AIC/BIC model selection
- Confidence intervals
- Model diagnostics

**Mathematics:**
```
ARIMA(p,d,q):
  (1 - φ₁B - ... - φₚBᵖ)(1-B)ᵈ Xₜ = (1 + θ₁B + ... + θ_qBᵈ)εₜ

Where:
  p = AR order (autoregressive)
  d = differencing order (integration)
  q = MA order (moving average)
```

---

### 2. SARIMA (Seasonal ARIMA)
**Best for:** Data with seasonal patterns (hourly, daily, weekly)

```python
from src.forecasting.time_series_models import SARIMAForecaster

sarima = SARIMAForecaster(
    order=(1,1,1),
    seasonal_order=(1,1,1,24)  # 24-hour seasonality
)

sarima.fit(volatility_data)
forecast = sarima.forecast(steps=10)
```

**Features:**
- Captures seasonal patterns
- Intraday volatility cycles
- Weekly/monthly patterns

**Mathematics:**
```
SARIMA(p,d,q)(P,D,Q)ₛ:
  Φ(Bˢ)φ(B)(1-Bˢ)ᴰ(1-B)ᵈXₜ = Θ(Bˢ)θ(B)εₜ

Where s = seasonal period
```

---

### 3. Prophet (Facebook)
**Best for:** Trend decomposition, multiple seasonalities

```python
from src.forecasting.time_series_models import ProphetForecaster

prophet = ProphetForecaster()

prophet.fit(volatility_data, timestamps)

# Forecast with trend + seasonality
forecast = prophet.forecast(periods=24, freq='5min')

print(forecast['forecast'])
print(forecast['trend'])
```

**Features:**
- Additive/multiplicative seasonality
- Trend changepoints
- Holiday effects
- Robust to missing data

**Components:**
```
y(t) = g(t) + s(t) + h(t) + εₜ

Where:
  g(t) = piecewise linear trend
  s(t) = seasonal components (Fourier series)
  h(t) = holiday effects
  εₜ = error term
```

---

### 4. Exponential Smoothing (Holt-Winters)
**Best for:** Weighted recent observations, level/trend/seasonality

```python
from src.forecasting.time_series_models import ExponentialSmoothingForecaster

exp_smooth = ExponentialSmoothingForecaster(
    seasonal='add',
    seasonal_periods=24
)

exp_smooth.fit(volatility_data)
forecast = exp_smooth.forecast(steps=10)
```

**Features:**
- Triple exponential smoothing
- Adaptive to recent changes
- Fast computation

**Equations:**
```
Level:  ℓₜ = α(yₜ - sₜ₋ₛ) + (1-α)(ℓₜ₋₁ + bₜ₋₁)
Trend:  bₜ = β(ℓₜ - ℓₜ₋₁) + (1-β)bₜ₋₁
Season: sₜ = γ(yₜ - ℓₜ) + (1-γ)sₜ₋ₛ
```

---

### 5. Ensemble Forecaster
**Best for:** Robust predictions, combining multiple models

```python
from src.forecasting.time_series_models import EnsembleForecaster

ensemble = EnsembleForecaster()

ensemble.fit(volatility_data, timestamps)

forecast = ensemble.forecast(steps=10)

print(f"Ensemble: {forecast['ensemble']}")
print(f"Weights: {forecast['weights']}")
print(f"Individual: {forecast['individual']}")
```

**Features:**
- Optimal weight calculation
- Inverse MSE weighting
- Combines ARIMA + Prophet + Exp Smoothing
- Robust to individual model failures

**Weighting:**
```
w_i = (1/MSE_i) / Σ(1/MSE_j)

Final forecast = Σ w_i · forecast_i
```

---

## 🚀 Quick Start

### Installation
```bash
pip install statsmodels prophet pmdarima
```

### Basic Usage
```python
import json
import numpy as np
from src.forecasting.time_series_models import EnsembleForecaster

# Load data
with open('data/results.json', 'r') as f:
    data = json.load(f)

neo_data = [d for d in data if d['pair'] == 'NEO/USDT']

# Extract volatility
vols = np.array([d['realized_vol'] for d in neo_data])
timestamps = [d['timestamp'] for d in neo_data]

# Forecast
ensemble = EnsembleForecaster()
ensemble.fit(vols, timestamps)
forecast = ensemble.forecast(steps=10)

print("10-step forecast:", forecast['ensemble'])
```

---

## 📈 Performance Comparison

| Model | Training Time | Forecast Speed | Accuracy* | Best For |
|-------|---------------|----------------|-----------|----------|
| ARIMA | 5-10s | <1ms | ⭐⭐⭐⭐ | Short-term |
| SARIMA | 10-20s | <1ms | ⭐⭐⭐⭐⭐ | Seasonal |
| Prophet | 2-5s | <1ms | ⭐⭐⭐⭐ | Trend |
| Exp Smooth | <1s | <1ms | ⭐⭐⭐ | Simple |
| Ensemble | 15-30s | 2-3ms | ⭐⭐⭐⭐⭐ | Robust |

*Accuracy on synthetic volatility data (RMSE)

---

## 🎯 Use Cases

### 1. Volatility Forecasting
```python
# Predict next 24 periods (2 hours at 5min intervals)
forecast = ensemble.forecast(steps=24)

# Get confidence bands
lower = forecast['individual']['arima']['lower_bound']
upper = forecast['individual']['arima']['upper_bound']
```

### 2. Risk Management
```python
# VaR calculation with forecasted volatility
vol_forecast = forecast['ensemble'][0]
position_size = 100000
var_95 = position_size * vol_forecast * 1.645  # 95% VaR
```

### 3. Trading Signals
```python
# Mean reversion signal
current_vol = vols[-1]
forecasted_vol = forecast['ensemble'][0]

if forecasted_vol < current_vol * 0.9:
    signal = "SELL_STRADDLE"  # Volatility expected to drop
elif forecasted_vol > current_vol * 1.1:
    signal = "BUY_STRADDLE"  # Volatility expected to rise
```

### 4. Backtesting
```python
# Walk-forward validation
errors = []
for i in range(50, len(vols)):
    train = vols[:i]
    test = vols[i]
    
    arima = ARIMAForecaster()
    arima.auto_arima(train)
    arima.fit(train)
    
    pred = arima.forecast(steps=1)['forecast'][0]
    errors.append((pred - test) ** 2)

rmse = np.sqrt(np.mean(errors))
print(f"Walk-forward RMSE: {rmse:.4f}")
```

---

## 🔧 Advanced Features

### Auto ARIMA
Automatically searches for best model:

```python
arima = ARIMAForecaster()

# Search parameters
arima.auto_arima(
    data,
    start_p=0, max_p=5,  # AR order range
    start_q=0, max_q=5,  # MA order range
    seasonal=False,
    d=None,  # Auto-detect differencing
    trace=True  # Show search progress
)

print(f"Best order: {arima.order}")
print(f"AIC: {arima.model.aic}")
```

### Model Diagnostics
```python
# Check residuals
arima.diagnose()  # Saves plots to data/

# Components plot (Prophet)
prophet.plot_components()
```

### Custom Seasonality
```python
# Add multiple seasonal patterns
prophet = Prophet()
prophet.add_seasonality(name='hourly', period=1, fourier_order=8)
prophet.add_seasonality(name='daily', period=1, fourier_order=10)
prophet.add_seasonality(name='weekly', period=7, fourier_order=3)
```

---

## 📊 Mathematical Background

### Stationarity
ARIMA requires stationary data:

**ADF Test (Augmented Dickey-Fuller):**
```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(volatility_data)
print(f"ADF Statistic: {result[0]}")
print(f"p-value: {result[1]}")

if result[1] < 0.05:
    print("Series is stationary")
else:
    print("Need differencing (d > 0)")
```

### ACF/PACF Plots
Determine ARIMA orders:

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plot_acf(volatility_data, lags=40)
plot_pacf(volatility_data, lags=40)
```

**Rules:**
- ACF cuts off at lag q → MA(q)
- PACF cuts off at lag p → AR(p)
- Both decay → ARMA(p,q)

### Information Criteria
Model selection:

```
AIC = -2·log(L) + 2·k
BIC = -2·log(L) + k·log(n)

Where:
  L = likelihood
  k = parameters
  n = observations
```

Lower is better!

---

## 🎓 Examples

### Example 1: Simple Forecast
```python
from src.forecasting.time_series_models import ARIMAForecaster
import numpy as np

# Generate sample data
data = np.random.randn(200) * 0.02 + 0.20

# Forecast
arima = ARIMAForecaster()
arima.auto_arima(data)
arima.fit(data)

forecast = arima.forecast(steps=10)
print("Next 10 values:", forecast['forecast'])
```

### Example 2: Ensemble with Weights
```python
from src.forecasting.time_series_models import EnsembleForecaster

ensemble = EnsembleForecaster()
ensemble.fit(volatility_data, timestamps)

result = ensemble.forecast(steps=10)

# Show contribution of each model
for model, weight in result['weights'].items():
    print(f"{model}: {weight:.1%} weight")
```

### Example 3: Confidence Intervals
```python
arima = ARIMAForecaster(order=(2,1,0))
arima.fit(data)

forecast = arima.forecast(steps=10)

# Plot
import matplotlib.pyplot as plt

plt.plot(forecast['forecast'], label='Forecast')
plt.fill_between(
    range(10),
    forecast['lower_bound'],
    forecast['upper_bound'],
    alpha=0.3,
    label='95% CI'
)
plt.legend()
plt.show()
```

---

## 🔬 Research Papers

1. **ARIMA:**
   - Box, G. E. P., & Jenkins, G. M. (1970). *Time Series Analysis: Forecasting and Control*

2. **SARIMA:**
   - Hyndman, R. J., & Athanasopoulos, G. (2018). *Forecasting: Principles and Practice*

3. **Prophet:**
   - Taylor, S. J., & Letham, B. (2018). "Forecasting at Scale"

4. **Exponential Smoothing:**
   - Holt, C. C. (2004). "Forecasting seasonals and trends by exponentially weighted moving averages"

---

## 💡 Tips & Tricks

### 1. Data Requirements
- **ARIMA:** Minimum 50-100 observations
- **SARIMA:** At least 2 full seasonal cycles
- **Prophet:** 100+ observations recommended
- **Ensemble:** 200+ for stable weights

### 2. Hyperparameter Tuning
```python
# Grid search for SARIMA
best_aic = float('inf')
best_params = None

for p in range(3):
    for q in range(3):
        for P in range(2):
            for Q in range(2):
                try:
                    model = SARIMAX(data, order=(p,1,q), seasonal_order=(P,1,Q,24))
                    results = model.fit(disp=False)
                    if results.aic < best_aic:
                        best_aic = results.aic
                        best_params = (p,1,q,P,1,Q,24)
                except:
                    continue

print(f"Best: {best_params}, AIC: {best_aic}")
```

### 3. Handling Missing Data
```python
# Prophet handles gaps automatically
# For ARIMA, interpolate first:
from scipy.interpolate import interp1d

x = np.arange(len(data))
mask = ~np.isnan(data)
f = interp1d(x[mask], data[mask], kind='linear', fill_value='extrapolate')
data_filled = f(x)
```

---

## 📚 Further Reading

- [statsmodels Documentation](https://www.statsmodels.org/)
- [Prophet Documentation](https://facebook.github.io/prophet/)
- [pmdarima Documentation](http://alkaline-ml.com/pmdarima/)

---

## 🏆 Integration with AgenticSpoons

```python
# In enhanced_demo.py
from src.forecasting.time_series_models import EnsembleForecaster

# After collecting volatility data
vol_forecaster = EnsembleForecaster()
vol_forecaster.fit(historical_vols, timestamps)

# Get next 10-period forecast
forecast = vol_forecaster.forecast(steps=10)

# Use in trading strategy
if forecast['ensemble'][0] > current_vol * 1.2:
    # High volatility expected - adjust position sizing
    position_size *= 0.5
```

---

**Built for Neo Blockchain Hackathon 2025** 📈🔮

*"From historical patterns to future predictions"*
