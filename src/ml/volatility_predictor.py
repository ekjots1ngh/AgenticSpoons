"""
ML-based Volatility Prediction
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib
from loguru import logger

class MLVolatilityPredictor:
    """Machine learning volatility forecaster"""
    
    def __init__(self, model_type='xgboost'):
        self.model_type = model_type
        self.model = None
        self.is_trained = False
        
    def create_features(self, data):
        """Feature engineering for volatility prediction"""
        df = pd.DataFrame(data)
        
        # Price features
        df['returns'] = df['price'].pct_change()
        df['log_returns'] = np.log(df['price'] / df['price'].shift(1))
        
        # If realized_vol is mostly NaN, calculate from returns
        if df['realized_vol'].isna().sum() > len(df) * 0.5:
            df['realized_vol'] = df['returns'].rolling(5).std()
        
        # Lagged volatility - use shorter windows to reduce NaNs
        df['rv_lag1'] = df['realized_vol'].shift(1)
        df['rv_lag2'] = df['realized_vol'].shift(2)
        
        # Rolling statistics
        df['price_ma_5'] = df['price'].rolling(5).mean()
        df['price_std_5'] = df['price'].rolling(5).std()
        df['volume_ma_5'] = df['volume'].rolling(5).mean() if 'volume' in df.columns else 0
        
        # Momentum
        df['momentum_5'] = df['price'] / df['price'].shift(5) - 1
        
        # Hour/day features (if timestamp available)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
        
        # Forward fill for volatility to propagate values
        df['realized_vol'] = df['realized_vol'].ffill()
        df['rv_lag1'] = df['rv_lag1'].ffill()
        df['rv_lag2'] = df['rv_lag2'].ffill()
        
        # Fill any remaining NaN with forward fill then backward fill
        df = df.ffill().bfill()
        
        # Define feature columns before dropping
        feature_cols = [
            'returns', 'log_returns',
            'rv_lag1', 'rv_lag2',
            'price_ma_5', 'price_std_5', 'volume_ma_5',
            'momentum_5', 'realized_vol'
        ]
        
        if 'hour' in df.columns:
            feature_cols.extend(['hour', 'day_of_week'])
        
        # Drop NaN ONLY in feature columns (not entire dataframe)
        df = df[feature_cols].dropna()
        
        return df
    
    def prepare_data(self, data):
        """Prepare data for training"""
        df = self.create_features(data)
        
        if len(df) < 10:
            logger.warning(f"Only {len(df)} samples available, need at least 10")
            raise ValueError("Not enough data samples after feature engineering")
        
        # Features - use only those we engineer
        feature_cols = [
            'returns', 'log_returns',
            'rv_lag1', 'rv_lag2',
            'price_ma_5', 'price_std_5', 'volume_ma_5',
            'momentum_5'
        ]
        
        # Add time features if available
        if 'hour' in df.columns:
            feature_cols.extend(['hour', 'day_of_week'])
        
        X = df[feature_cols].values
        y = df['realized_vol'].values
        
        logger.info(f"Prepared {len(X)} samples with {len(feature_cols)} features")
        
        return X, y
    
    def train(self, data, test_size=0.2):
        """Train ML model"""
        logger.info(f"Training {self.model_type} model...")
        
        X, y = self.prepare_data(data)
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, shuffle=False
        )
        
        # Choose model
        if self.model_type == 'xgboost':
            self.model = XGBRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        elif self.model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
        else:
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
        
        # Train
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.is_trained = True
        
        logger.success(f"Model trained! R² = {r2:.3f}, RMSE = {np.sqrt(mse):.4f}")
        
        return {
            'r2_score': r2,
            'rmse': np.sqrt(mse),
            'test_size': len(y_test)
        }
    
    def predict(self, data):
        """Predict next volatility"""
        if not self.is_trained:
            raise ValueError("Model not trained yet!")
        
        df = self.create_features(data)
        
        feature_cols = [
            'returns', 'log_returns',
            'rv_lag1', 'rv_lag2',
            'price_ma_5', 'price_std_5', 'volume_ma_5',
            'momentum_5'
        ]
        
        if 'hour' in df.columns:
            feature_cols.extend(['hour', 'day_of_week'])
        
        X = df[feature_cols].iloc[-1:].values
        
        prediction = self.model.predict(X)[0]
        
        return float(prediction)
    
    def save_model(self, path='models/ml_vol_predictor.pkl'):
        """Save trained model"""
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.model, path)
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path='models/ml_vol_predictor.pkl'):
        """Load trained model"""
        self.model = joblib.load(path)
        self.is_trained = True
        logger.info(f"Model loaded from {path}")
    
    def feature_importance(self):
        """Get feature importance"""
        if not self.is_trained:
            return None
        
        if hasattr(self.model, 'feature_importances_'):
            importance = self.model.feature_importances_
            
            features = [
                'returns', 'log_returns',
                'rv_lag1', 'rv_lag2',
                'price_ma_5', 'price_std_5', 'volume_ma_5',
                'momentum_5'
            ]
            
            return dict(zip(features, importance))
        
        return None

# Create training script
def train_ml_model():
    """Train ML model on current data"""
    import json
    
    # Load data
    with open('data/results.json', 'r') as f:
        data = json.load(f)
    
    neo_data = [d for d in data if d['pair'] == 'NEO/USDT']
    
    if len(neo_data) < 100:
        print("❌ Need at least 100 data points")
        return
    
    # Train
    predictor = MLVolatilityPredictor(model_type='xgboost')
    metrics = predictor.train(neo_data)
    
    print(f"\n✅ Model Trained!")
    print(f"   R² Score: {metrics['r2_score']:.3f}")
    print(f"   RMSE: {metrics['rmse']:.4f}")
    
    # Feature importance
    importance = predictor.feature_importance()
    if importance:
        print("\n📊 Feature Importance:")
        for feat, imp in sorted(importance.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {feat}: {imp:.3f}")
    
    # Save
    predictor.save_model()
    
    # Test prediction
    next_vol = predictor.predict(neo_data)
    print(f"\n🔮 Next Period Prediction: {next_vol:.2%}")

if __name__ == "__main__":
    train_ml_model()
