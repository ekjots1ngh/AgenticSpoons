"""
Advanced Machine Learning for Volatility Prediction
- LSTM (Long Short-Term Memory) for time series
- Transformer for sequence modeling
- Ensemble methods
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import Ridge
import joblib
from loguru import logger

# ========== LSTM MODEL ==========
def create_lstm_model():
    """Create LSTM model for volatility forecasting"""
    try:
        from tensorflow import keras
        from tensorflow.keras import layers
        
        model = keras.Sequential([
            layers.LSTM(64, return_sequences=True, input_shape=(30, 10)),
            layers.Dropout(0.2),
            layers.LSTM(32, return_sequences=False),
            layers.Dropout(0.2),
            layers.Dense(16, activation='relu'),
            layers.Dense(1)
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    except ImportError:
        logger.warning("TensorFlow not available")
        return None

class LSTMVolatilityPredictor:
    """LSTM-based volatility predictor"""
    
    def __init__(self, lookback=30, features=10):
        self.lookback = lookback
        self.features = features
        self.model = create_lstm_model()
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def prepare_sequences(self, data):
        """Create sequences for LSTM"""
        df = pd.DataFrame(data)
        
        # Feature engineering
        df['returns'] = df['price'].pct_change()
        df['log_returns'] = np.log(df['price'] / df['price'].shift(1))
        df['rv_lag1'] = df['realized_vol'].shift(1)
        df['rv_lag2'] = df['realized_vol'].shift(2)
        df['rv_ma5'] = df['realized_vol'].rolling(5).mean()
        df['rv_std5'] = df['realized_vol'].rolling(5).std()
        df['price_ma10'] = df['price'].rolling(10).mean()
        df['volume_ma5'] = df.get('volume', pd.Series([0]*len(df))).rolling(5).mean()
        df['momentum'] = df['price'] / df['price'].shift(5) - 1
        
        df = df.dropna()
        
        # Select features
        feature_cols = [
            'returns', 'log_returns', 'rv_lag1', 'rv_lag2',
            'rv_ma5', 'rv_std5', 'price_ma10', 'volume_ma5', 'momentum'
        ]
        
        X_raw = df[feature_cols].values
        y_raw = df['realized_vol'].values
        
        # Scale
        X_scaled = self.scaler.fit_transform(X_raw)
        
        # Create sequences
        X, y = [], []
        for i in range(len(X_scaled) - self.lookback):
            X.append(X_scaled[i:i+self.lookback])
            y.append(y_raw[i+self.lookback])
        
        return np.array(X), np.array(y)
    
    def train(self, data, epochs=50, validation_split=0.2):
        """Train LSTM model"""
        if self.model is None:
            logger.error("TensorFlow not available")
            return
        
        X, y = self.prepare_sequences(data)
        
        logger.info(f"Training LSTM with {len(X)} sequences...")
        
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=32,
            validation_split=validation_split,
            verbose=0
        )
        
        self.is_trained = True
        
        final_loss = history.history['loss'][-1]
        final_mae = history.history['mae'][-1]
        
        logger.success(f"LSTM trained! Loss={final_loss:.6f}, MAE={final_mae:.6f}")
        
        return history
    
    def predict(self, data):
        """Predict next volatility"""
        if not self.is_trained:
            raise ValueError("Model not trained")
        
        X, _ = self.prepare_sequences(data)
        prediction = self.model.predict(X[-1:], verbose=0)
        
        return float(prediction[0][0])

# ========== TRANSFORMER MODEL ==========
class TransformerVolatility:
    """Transformer-based volatility prediction"""
    
    def __init__(self, seq_length=50, d_model=64, n_heads=4):
        self.seq_length = seq_length
        self.d_model = d_model
        self.n_heads = n_heads
        self.model = None
    
    def create_model(self):
        """Create Transformer architecture"""
        try:
            from tensorflow import keras
            from tensorflow.keras import layers
            
            inputs = layers.Input(shape=(self.seq_length, 10))
            
            # Positional encoding
            x = layers.Dense(self.d_model)(inputs)
            
            # Multi-head attention
            attention = layers.MultiHeadAttention(
                num_heads=self.n_heads,
                key_dim=self.d_model // self.n_heads
            )(x, x)
            
            # Add & Norm
            x = layers.Add()([x, attention])
            x = layers.LayerNormalization()(x)
            
            # Feed-forward
            ff = layers.Dense(self.d_model * 2, activation='relu')(x)
            ff = layers.Dense(self.d_model)(ff)
            
            # Add & Norm
            x = layers.Add()([x, ff])
            x = layers.LayerNormalization()(x)
            
            # Output
            x = layers.GlobalAveragePooling1D()(x)
            x = layers.Dense(32, activation='relu')(x)
            outputs = layers.Dense(1)(x)
            
            model = keras.Model(inputs=inputs, outputs=outputs)
            model.compile(optimizer='adam', loss='mse', metrics=['mae'])
            
            return model
        except ImportError:
            logger.warning("TensorFlow not available")
            return None

# ========== ENSEMBLE MODEL ==========
class EnsembleVolatility:
    """Ensemble of multiple models"""
    
    def __init__(self):
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        try:
            from xgboost import XGBRegressor
        except ImportError:
            logger.warning("XGBoost not available, using GBM instead")
            XGBRegressor = GradientBoostingRegressor
        
        try:
            from lightgbm import LGBMRegressor
        except ImportError:
            logger.warning("LightGBM not available, using RF instead")
            LGBMRegressor = RandomForestRegressor
        
        # Base models
        self.models = {
            'rf': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
            'gbm': GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42),
            'xgb': XGBRegressor(n_estimators=100, max_depth=5, random_state=42) if XGBRegressor != GradientBoostingRegressor else GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42),
            'lgbm': LGBMRegressor(n_estimators=100, max_depth=5, random_state=42, verbose=-1) if LGBMRegressor != RandomForestRegressor else RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        }
        
        # Meta-learner
        self.meta_model = Ridge(alpha=1.0)
        self.is_trained = False
        self.feature_cols = []
    
    def prepare_features(self, data):
        """Feature engineering"""
        df = pd.DataFrame(data)
        
        # Price features
        df['returns'] = df['price'].pct_change()
        df['log_returns'] = np.log(df['price'] / df['price'].shift(1))
        
        # Lagged volatility
        for lag in [1, 2, 3, 5, 10]:
            df[f'rv_lag{lag}'] = df['realized_vol'].shift(lag)
        
        # Rolling statistics
        for window in [5, 10, 20]:
            df[f'rv_ma{window}'] = df['realized_vol'].rolling(window).mean()
            df[f'rv_std{window}'] = df['realized_vol'].rolling(window).std()
            df[f'price_ma{window}'] = df['price'].rolling(window).mean()
        
        # Volatility of volatility
        df['vol_of_vol'] = df['realized_vol'].rolling(10).std()
        
        # Momentum
        for period in [5, 10, 20]:
            df[f'momentum{period}'] = df['price'] / df['price'].shift(period) - 1
        
        # Realized variance
        df['realized_variance'] = df['realized_vol'] ** 2
        
        df = df.dropna()
        
        feature_cols = [col for col in df.columns if col not in ['timestamp', 'pair', 'price', 'realized_vol']]
        
        X = df[feature_cols].values
        y = df['realized_vol'].values
        
        return X, y, feature_cols
    
    def train(self, data, test_size=0.2):
        """Train ensemble model"""
        from sklearn.model_selection import train_test_split
        
        X, y, feature_cols = self.prepare_features(data)
        self.feature_cols = feature_cols
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, shuffle=False
        )
        
        logger.info("Training ensemble models...")
        
        # Train base models
        predictions_train = np.zeros((len(X_train), len(self.models)))
        predictions_test = np.zeros((len(X_test), len(self.models)))
        
        for i, (name, model) in enumerate(self.models.items()):
            logger.info(f"  Training {name}...")
            model.fit(X_train, y_train)
            
            predictions_train[:, i] = model.predict(X_train)
            predictions_test[:, i] = model.predict(X_test)
        
        # Train meta-model
        logger.info("Training meta-model...")
        self.meta_model.fit(predictions_train, y_train)
        
        # Evaluate
        final_pred = self.meta_model.predict(predictions_test)
        
        from sklearn.metrics import mean_squared_error, r2_score
        
        mse = mean_squared_error(y_test, final_pred)
        r2 = r2_score(y_test, final_pred)
        
        self.is_trained = True
        
        logger.success(f"Ensemble trained! R²={r2:.3f}, RMSE={np.sqrt(mse):.6f}")
        
        return {
            'r2_score': r2,
            'rmse': np.sqrt(mse),
            'feature_importance': self.get_feature_importance()
        }
    
    def predict(self, data):
        """Predict using ensemble"""
        if not self.is_trained:
            raise ValueError("Model not trained")
        
        X, _, _ = self.prepare_features(data)
        
        # Get predictions from base models
        base_predictions = np.zeros((1, len(self.models)))
        
        for i, model in enumerate(self.models.values()):
            base_predictions[0, i] = model.predict(X[-1:])
        
        # Meta prediction
        final_pred = self.meta_model.predict(base_predictions)
        
        return float(final_pred[0])
    
    def get_feature_importance(self):
        """Get feature importance from tree models"""
        importance_dict = {}
        
        for name in ['rf', 'gbm', 'xgb', 'lgbm']:
            model = self.models[name]
            if hasattr(model, 'feature_importances_'):
                importance = model.feature_importances_
                importance_dict[name] = dict(zip(self.feature_cols, importance))
        
        return importance_dict

# ========== TRAINING SCRIPT ==========
def train_all_models():
    """Train all ML models"""
    import json
    import os
    
    if not os.path.exists('data/results.json'):
        print("❌ No data file found. Run enhanced_demo.py first.")
        return
    
    with open('data/results.json', 'r') as f:
        data = json.load(f)
    
    neo_data = [d for d in data if d['pair'] == 'NEO/USDT']
    
    if len(neo_data) < 200:
        print(f"❌ Need at least 200 data points, found {len(neo_data)}")
        return
    
    print("="*70)
    print("🤖 TRAINING ADVANCED ML MODELS")
    print("="*70)
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # 1. LSTM
    print("\n1. LSTM Model")
    print("-"*70)
    lstm = LSTMVolatilityPredictor()
    if lstm.model:
        lstm.train(neo_data, epochs=30)
        pred = lstm.predict(neo_data)
        print(f"   Next prediction: {pred:.2%}")
        lstm.model.save('models/lstm_volatility.h5')
        print("   ✓ Model saved: models/lstm_volatility.h5")
    else:
        print("   ⚠ TensorFlow not installed, skipping LSTM")
    
    # 2. Ensemble
    print("\n2. Ensemble Model")
    print("-"*70)
    ensemble = EnsembleVolatility()
    results = ensemble.train(neo_data)
    pred = ensemble.predict(neo_data)
    print(f"   Next prediction: {pred:.2%}")
    joblib.dump(ensemble, 'models/ensemble_volatility.pkl')
    print("   ✓ Model saved: models/ensemble_volatility.pkl")
    
    print("\n" + "="*70)
    print("✅ All models trained!")
    print("="*70)
    print(f"\nEnsemble Results:")
    print(f"  R² Score: {results['r2_score']:.3f}")
    print(f"  RMSE: {results['rmse']:.6f}")

if __name__ == "__main__":
    train_all_models()
