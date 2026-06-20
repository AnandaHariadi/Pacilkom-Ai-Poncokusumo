import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os

# Global variables to hold model state
_model = None
_features = None
_df_weather = None
_metrics = None

def get_weather_data():
    """Load and prepare the weather classification dataset."""
    global _df_weather, _model, _features, _metrics
    
    if _df_weather is not None:
        return _df_weather
        
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "..", "data", "cuaca", "data_cuaca_panen.csv")
    if not os.path.exists(csv_path):
        return pd.DataFrame() # Return empty if not found
        
    df = pd.read_csv(csv_path)
    
    # Simulate 'Hasil_Panen' (Harvest Yield in Tons) based on weather
    # Ideal conditions: Temp 20-30C, Humidity 60-80%, Moderate Precipitation
    np.random.seed(42)
    def simulate_yield(row):
        base = 50.0
        # Temp factor
        if 20 <= row['Temperature'] <= 30:
            base += 10
        else:
            base -= abs(25 - row['Temperature']) * 0.5
            
        # Humidity factor
        if 60 <= row['Humidity'] <= 80:
            base += 5
        else:
            base -= abs(70 - row['Humidity']) * 0.2
            
        # Precipitation factor
        if 40 <= row['Precipitation (%)'] <= 70:
            base += 15
        else:
            base -= abs(55 - row['Precipitation (%)']) * 0.1
            
        # Random noise
        base += np.random.normal(0, 3)
        return max(5.0, round(base, 2))
        
    df['Hasil_Panen'] = df.apply(simulate_yield, axis=1)
    _df_weather = df
    return df

def train_or_get_model():
    """Trains a Random Forest Regressor on the weather data."""
    global _model, _features, _metrics, _df_weather
    
    if _model is not None:
        return _model, _features, _metrics
        
    df = get_weather_data()
    if df.empty:
        return None, None, None
        
    _features = ['Temperature', 'Humidity', 'Wind Speed', 'Precipitation (%)', 'UV Index']
    X = df[_features]
    y = df['Hasil_Panen']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    _metrics = {
        'RMSE': round(np.sqrt(mean_squared_error(y_test, y_pred)), 2),
        'MAE': round(mean_absolute_error(y_test, y_pred), 2),
        'R2': round(r2_score(y_test, y_pred), 2)
    }
    
    _model = model
    return _model, _features, _metrics

def predict_panen_jst(suhu, kelembapan, kecepatan_angin, curah_hujan, uv_index):
    """Predict using the trained RandomForest model."""
    model, features, _ = train_or_get_model()
    if model is None:
        # Fallback to dummy
        return 45.5 + (suhu * 0.1)
        
    input_df = pd.DataFrame([[suhu, kelembapan, kecepatan_angin, curah_hujan, uv_index]], columns=features)
    prediksi = model.predict(input_df)[0]
    return round(prediksi, 2)

def get_historical_predictions(suhu=25.0, kelembapan=75.0, kecepatan_angin=10.0, curah_hujan=60.0, uv_index=5):
    """Return historical mock prediction for trend line centered around user inputs."""
    model, features, _ = train_or_get_model()
    
    # Generate 30 days of data centered around the input values
    waktu = [f'Hari {i}' for i in range(1, 31)]
    
    data = {
        'Temperature': np.clip([np.random.normal(suhu, 2.0) for _ in range(30)], 10, 40),
        'Humidity': np.clip([np.random.normal(kelembapan, 5.0) for _ in range(30)], 0, 100),
        'Wind Speed': np.clip([np.random.normal(kecepatan_angin, 2.0) for _ in range(30)], 0, 50),
        'Precipitation (%)': np.clip([np.random.normal(curah_hujan, 10.0) for _ in range(30)], 0, 100),
        'UV Index': np.clip([np.random.normal(uv_index, 1.0) for _ in range(30)], 0, 15),
    }
    df_sample = pd.DataFrame(data)
    
    pred_values = model.predict(df_sample[features])
    prediksi = pred_values.tolist()
    
    # Simulate actual values as prediction + some noise
    aktual = [p + np.random.normal(0, 3) for p in prediksi]
    
    return waktu, aktual, prediksi
