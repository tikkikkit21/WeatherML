import pandas as pd
import numpy as np
import joblib

model = joblib.load('models/best.model')
scaler = joblib.load('models/best.scaler')

def predict(temp: int, feels_like: int, humidity: float, uv: int, wind: int, gusts: int, season: str) -> None:
    # process data
    valid_seasons = ['fall', 'winter', 'spring', 'summer']
    season_encoding = {s: s == season for s in valid_seasons}
    if float(humidity) > 1.0:
        humidity = float(humidity) / 100

    # create sample df
    data = [temp, feels_like, humidity, uv, wind, gusts, *season_encoding.values()]
    columns = ['Temp', 'Feels Like', 'Humidity', 'UV', 'Wind', 'Gusts', 'Season_Fall', 'Season_Spring', 'Season_Summer', 'Season_Winter']
    df_sample = pd.DataFrame([data], columns=columns)
    
    # scale numerical data
    numeric_columns = df_sample.select_dtypes(include=['number']).columns
    df_sample[numeric_columns] = scaler.transform(df_sample[numeric_columns])
    
    # Make predictions
    prediction = model.predict(df_sample)[0]
    confidence = max(model.predict_proba(df_sample)[0])
    
    print(f'Prediction: {prediction}')
    print(f'Confidence: {confidence:.2%}')


if __name__ == '__main__':
    predict(73, 70, 0.5, 5, 4, 6, 'fall')
