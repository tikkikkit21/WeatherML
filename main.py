import pandas as pd
import joblib

model = joblib.load('models/best.model')
scaler = joblib.load('models/best.scaler')

def predict(temp: int, feels_like: int, humidity: float, uv: int, wind: int, gusts: int, season: str) -> None:
    # validate data
    valid_seasons = ['fall', 'winter', 'spring', 'summer']
    if season not in valid_seasons:
        print(f"Error: Invalid season '{season}'. Valid options are: [{', '.join(valid_seasons)}]")
        return
    
    # process data
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
    print('Welcome to WeatherML!')

    temp = input('What is the actual temperature (°F)? ')
    feels_like = input('What is the feels like temperature (°F)? ')
    humidity = input('What is the humidity (%)? ')
    uv = input('What is the UV? ')
    wind = input('What is the wind speed (mph)? ')
    gusts = input('What is the gusts speed (mph)? ')
    season = input('What is the season? ')
    
    print()
    predict(
        int(temp),
        int(feels_like),
        float(humidity),
        int(uv),
        int(wind),
        int(gusts),
        season
    )
