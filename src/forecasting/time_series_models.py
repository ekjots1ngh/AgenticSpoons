"""
Advanced Time Series Forecasting
- ARIMA (AutoRegressive Integrated Moving Average)
- SARIMA (Seasonal ARIMA)
- Prophet (Facebook)
- Exponential Smoothing
"""
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet
import pmdarima as pm
from loguru import logger
import warnings
warnings.filterwarnings('ignore')

class ARIMAForecaster:
    """ARIMA model for volatility forecasting"""
    
    def __init__(self, order=(1, 1, 1)):
        self.order = order
        self.model = None
        self.is_fitted = False
    
    def auto_arima(self, data, seasonal=False):
        """Automatically find best ARIMA parameters"""
        logger.info("Running auto ARIMA...")
        
        auto_model = pm.auto_arima(
            data,
            start_p=0, start_q=0,
            max_p=5, max_q=5,
            m=12 if seasonal else 1,
            seasonal=seasonal,
            d=None,  # Let auto_arima determine
            trace=False,
            error_action='ignore',
            suppress_warnings=True,
            stepwise=True
        )
        
        self.order = auto_model.order
        logger.success(f"Best ARIMA order: {self.order}")
        
        return self.order
    
    def fit(self, data):
        """Fit ARIMA model"""
        logger.info(f"Fitting ARIMA{self.order}...")
        
        self.model = ARIMA(data, order=self.order)
        self.model = self.model.fit()
        
        self.is_fitted = True
        
        logger.success(f"ARIMA fitted! AIC={self.model.aic:.2f}")
        
        return {
            'aic': self.model.aic,
            'bic': self.model.bic,
            'params': dict(self.model.params)
        }
    
    def forecast(self, steps=10):
        """Forecast future values"""
        if not self.is_fitted:
            raise ValueError("Model not fitted")
        
        forecast = self.model.forecast(steps=steps)
        
        # Get confidence intervals
        forecast_obj = self.model.get_forecast(steps=steps)
        conf_int = forecast_obj.conf_int()
        
        return {
            'forecast': forecast.values if hasattr(forecast, 'values') else forecast,
            'lower_bound': conf_int.iloc[:, 0].values,
            'upper_bound': conf_int.iloc[:, 1].values
        }
    
    def diagnose(self):
        """Model diagnostics"""
        if not self.is_fitted:
            return None
        
        import matplotlib.pyplot as plt
        
        fig = self.model.plot_diagnostics(figsize=(12, 8))
        plt.savefig('data/arima_diagnostics.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info("Diagnostics saved to data/arima_diagnostics.png")

class SARIMAForecaster:
    """SARIMA - for seasonal patterns"""
    
    def __init__(self, order=(1,1,1), seasonal_order=(1,1,1,12)):
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None
        self.is_fitted = False
    
    def fit(self, data):
        """Fit SARIMA model"""
        logger.info(f"Fitting SARIMA{self.order}x{self.seasonal_order}...")
        
        self.model = SARIMAX(
            data,
            order=self.order,
            seasonal_order=self.seasonal_order
        )
        self.model = self.model.fit(disp=False)
        
        self.is_fitted = True
        
        logger.success(f"SARIMA fitted! AIC={self.model.aic:.2f}")
        
        return {
            'aic': self.model.aic,
            'bic': self.model.bic
        }
    
    def forecast(self, steps=10):
        """Forecast with SARIMA"""
        if not self.is_fitted:
            raise ValueError("Model not fitted")
        
        forecast = self.model.forecast(steps=steps)
        
        return forecast.values if hasattr(forecast, 'values') else forecast

class ProphetForecaster:
    """Facebook Prophet for volatility"""
    
    def __init__(self):
        self.model = Prophet(
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10.0,
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False
        )
        self.is_fitted = False
    
    def prepare_data(self, data, timestamps):
        """Prepare data in Prophet format"""
        df = pd.DataFrame({
            'ds': pd.to_datetime(timestamps),
            'y': data
        })
        return df
    
    def fit(self, data, timestamps):
        """Fit Prophet model"""
        logger.info("Fitting Prophet model...")
        
        df = self.prepare_data(data, timestamps)
        
        # Add custom seasonality for intraday patterns
        self.model.add_seasonality(
            name='hourly',
            period=1,
            fourier_order=8
        )
        
        self.model.fit(df)
        
        self.is_fitted = True
        
        logger.success("Prophet fitted!")
        
        return self
    
    def forecast(self, periods=10, freq='5min'):
        """Forecast future values"""
        if not self.is_fitted:
            raise ValueError("Model not fitted")
        
        future = self.model.make_future_dataframe(
            periods=periods,
            freq=freq
        )
        
        forecast = self.model.predict(future)
        
        return {
            'forecast': forecast['yhat'].tail(periods).values,
            'lower_bound': forecast['yhat_lower'].tail(periods).values,
            'upper_bound': forecast['yhat_upper'].tail(periods).values,
            'trend': forecast['trend'].tail(periods).values
        }
    
    def plot_components(self):
        """Plot forecast components"""
        import matplotlib.pyplot as plt
        
        future = self.model.make_future_dataframe(periods=24, freq='5min')
        forecast = self.model.predict(future)
        
        fig = self.model.plot_components(forecast)
        plt.savefig('data/prophet_components.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info("Components saved to data/prophet_components.png")

class ExponentialSmoothingForecaster:
    """Triple Exponential Smoothing (Holt-Winters)"""
    
    def __init__(self, seasonal='add', seasonal_periods=24):
        self.seasonal = seasonal
        self.seasonal_periods = seasonal_periods
        self.model = None
        self.is_fitted = False
    
    def fit(self, data):
        """Fit exponential smoothing"""
        logger.info("Fitting Exponential Smoothing...")
        
        try:
            self.model = ExponentialSmoothing(
                data,
                seasonal=self.seasonal,
                seasonal_periods=self.seasonal_periods,
                trend='add'
            )
            
            self.model = self.model.fit()
            
            self.is_fitted = True
            
            logger.success("Exponential Smoothing fitted!")
        except Exception as e:
            logger.warning(f"Exponential Smoothing failed: {e}, using simple model")
            # Fallback to non-seasonal
            self.model = ExponentialSmoothing(data, trend='add', seasonal=None)
            self.model = self.model.fit()
            self.is_fitted = True
        
        return self
    
    def forecast(self, steps=10):
        """Forecast future values"""
        if not self.is_fitted:
            raise ValueError("Model not fitted")
        
        forecast = self.model.forecast(steps=steps)
        
        return forecast.values if hasattr(forecast, 'values') else forecast

class EnsembleForecaster:
    """Ensemble of multiple forecasting models"""
    
    def __init__(self):
        self.models = {
            'arima': ARIMAForecaster(),
            'exp_smooth': ExponentialSmoothingForecaster(seasonal_periods=12)
        }
        self.weights = None
        self.prophet_available = False
    
    def fit(self, data, timestamps=None):
        """Fit all models"""
        logger.info("Fitting ensemble models...")
        
        # ARIMA
        try:
            self.models['arima'].auto_arima(data)
            self.models['arima'].fit(data)
        except Exception as e:
            logger.warning(f"ARIMA failed: {e}")
        
        # Prophet (optional, needs timestamps)
        if timestamps is not None and len(timestamps) == len(data):
            try:
                prophet = ProphetForecaster()
                prophet.fit(data, timestamps)
                self.models['prophet'] = prophet
                self.prophet_available = True
            except Exception as e:
                logger.warning(f"Prophet failed: {e}")
        
        # Exponential Smoothing
        try:
            self.models['exp_smooth'].fit(data)
        except Exception as e:
            logger.warning(f"Exp Smoothing failed: {e}")
        
        # Calculate weights based on in-sample fit
        self.weights = self._calculate_weights(data)
        
        logger.success(f"Ensemble fitted with {len(self.weights)} models!")
        
        return self
    
    def _calculate_weights(self, data):
        """Calculate optimal weights"""
        from sklearn.metrics import mean_squared_error
        
        # Split data for validation
        train_size = int(len(data) * 0.8)
        test_data = data[train_size:]
        test_size = len(test_data)
        
        errors = {}
        
        # ARIMA error
        try:
            if self.models['arima'].is_fitted:
                arima_forecast = self.models['arima'].forecast(steps=test_size)
                errors['arima'] = mean_squared_error(test_data, arima_forecast['forecast'])
        except Exception as e:
            logger.debug(f"ARIMA validation error: {e}")
            errors['arima'] = float('inf')
        
        # Prophet error
        if self.prophet_available:
            try:
                prophet_forecast = self.models['prophet'].forecast(periods=test_size)
                errors['prophet'] = mean_squared_error(test_data, prophet_forecast['forecast'])
            except Exception as e:
                logger.debug(f"Prophet validation error: {e}")
                errors['prophet'] = float('inf')
        
        # Exp Smoothing error
        try:
            if self.models['exp_smooth'].is_fitted:
                exp_forecast = self.models['exp_smooth'].forecast(steps=test_size)
                errors['exp_smooth'] = mean_squared_error(test_data, exp_forecast)
        except Exception as e:
            logger.debug(f"Exp Smoothing validation error: {e}")
            errors['exp_smooth'] = float('inf')
        
        # Inverse error weighting
        valid_errors = {k: v for k, v in errors.items() if v < float('inf')}
        
        if not valid_errors:
            # Equal weights if no valid models
            return {model: 1.0 / len(self.models) for model in self.models}
        
        total_inv_error = sum(1.0 / e for e in valid_errors.values())
        
        weights = {
            model: (1.0 / errors[model] / total_inv_error if model in valid_errors else 0)
            for model in self.models
        }
        
        logger.info(f"Ensemble weights: {weights}")
        
        return weights
    
    def forecast(self, steps=10):
        """Combined forecast"""
        forecasts = {}
        
        # Get individual forecasts
        try:
            if self.models['arima'].is_fitted:
                forecasts['arima'] = self.models['arima'].forecast(steps)['forecast']
        except Exception as e:
            logger.warning(f"ARIMA forecast failed: {e}")
        
        if self.prophet_available:
            try:
                forecasts['prophet'] = self.models['prophet'].forecast(periods=steps)['forecast']
            except Exception as e:
                logger.warning(f"Prophet forecast failed: {e}")
        
        try:
            if self.models['exp_smooth'].is_fitted:
                forecasts['exp_smooth'] = self.models['exp_smooth'].forecast(steps)
        except Exception as e:
            logger.warning(f"Exp Smoothing forecast failed: {e}")
        
        if not forecasts:
            logger.error("No forecasts available!")
            return {
                'ensemble': np.zeros(steps),
                'individual': {},
                'weights': self.weights
            }
        
        # Weighted average
        ensemble_forecast = np.zeros(steps)
        
        for model, forecast in forecasts.items():
            weight = self.weights.get(model, 0)
            ensemble_forecast += weight * np.array(forecast)
        
        return {
            'ensemble': ensemble_forecast,
            'individual': forecasts,
            'weights': self.weights
        }

# ========== TESTING SCRIPT ==========
def run_forecasting_tests():
    """Test all forecasting models"""
    import json
    import os
    
    print("\n" + "="*70)
    print("📈 TIME SERIES FORECASTING")
    print("="*70)
    
    # Check if data exists
    if not os.path.exists('data/results.json'):
        print("\n❌ No data found. Run enhanced_demo.py first to generate data.")
        print("   python src/enhanced_demo.py")
        return
    
    with open('data/results.json', 'r') as f:
        data = json.load(f)
    
    # Filter for one pair
    neo_data = [d for d in data if d['pair'] == 'NEO/USDT']
    
    if len(neo_data) < 100:
        print(f"\n❌ Need at least 100 data points, found {len(neo_data)}")
        print("   Run enhanced_demo.py for 300+ seconds to collect enough data")
        return
    
    print(f"\n✅ Found {len(neo_data)} data points for NEO/USDT")
    
    # Extract volatility series
    vols = np.array([d['realized_vol'] for d in neo_data])
    timestamps = [d['timestamp'] for d in neo_data]
    
    # Test 1: ARIMA
    print("\n1️⃣  ARIMA Forecasting")
    print("-"*70)
    
    try:
        arima = ARIMAForecaster()
        arima.auto_arima(vols)
        arima.fit(vols)
        forecast = arima.forecast(steps=10)
        
        print(f"   Order: {arima.order}")
        print(f"   10-step forecast: {forecast['forecast'][:5]}...")
        print(f"   Confidence: [{forecast['lower_bound'][0]:.4f}, {forecast['upper_bound'][0]:.4f}]")
        print("   ✅ ARIMA completed")
    except Exception as e:
        print(f"   ❌ ARIMA failed: {e}")
    
    # Test 2: Prophet
    print("\n2️⃣  Prophet Forecasting")
    print("-"*70)
    
    try:
        prophet = ProphetForecaster()
        prophet.fit(vols, timestamps)
        prophet_forecast = prophet.forecast(periods=10, freq='5min')
        
        print(f"   10-period forecast: {prophet_forecast['forecast'][:5]}...")
        print(f"   Trend: {prophet_forecast['trend'][:3]}...")
        print("   ✅ Prophet completed")
    except Exception as e:
        print(f"   ❌ Prophet failed: {e}")
    
    # Test 3: Exponential Smoothing
    print("\n3️⃣  Exponential Smoothing")
    print("-"*70)
    
    try:
        exp_smooth = ExponentialSmoothingForecaster()
        exp_smooth.fit(vols)
        exp_forecast = exp_smooth.forecast(steps=10)
        
        print(f"   10-step forecast: {exp_forecast[:5]}...")
        print("   ✅ Exponential Smoothing completed")
    except Exception as e:
        print(f"   ❌ Exponential Smoothing failed: {e}")
    
    # Test 4: Ensemble
    print("\n4️⃣  Ensemble Forecasting")
    print("-"*70)
    
    try:
        ensemble = EnsembleForecaster()
        ensemble.fit(vols, timestamps)
        ensemble_forecast = ensemble.forecast(steps=10)
        
        print(f"   Ensemble forecast: {ensemble_forecast['ensemble'][:5]}...")
        print(f"   Model weights:")
        for model, weight in ensemble_forecast['weights'].items():
            print(f"      {model:12s}: {weight:.3f}")
        print("   ✅ Ensemble completed")
    except Exception as e:
        print(f"   ❌ Ensemble failed: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("✅ Time Series Forecasting Tests Complete!")
    print("="*70)
    
    print("\nModels Available:")
    print("   • ARIMA: Auto-tuned AR/MA parameters")
    print("   • SARIMA: Seasonal patterns")
    print("   • Prophet: Trend + seasonality decomposition")
    print("   • Exponential Smoothing: Holt-Winters")
    print("   • Ensemble: Weighted combination")
    
    print("\nUse Cases:")
    print("   • Volatility forecasting (next 10 periods)")
    print("   • Trend detection and seasonality")
    print("   • Confidence intervals for risk management")
    print("   • Multi-step ahead predictions")

if __name__ == "__main__":
    run_forecasting_tests()
