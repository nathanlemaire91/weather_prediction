import datetime
import numpy as np
import pandas as pd

from db_engine import db_engine
from utils import get_env_variable, open_joblib_s3



def get_predict_data(data):
    current_date = datetime.datetime.now()
    current_date_minus_1_day = current_date - datetime.timedelta(days=1)

    query = f"""
    SELECT * FROM weather_data WHERE timestamp >= '{current_date_minus_1_day}' \
        AND timestamp <= '{current_date}' ORDER BY timestamp ASC
    """

    raw_data = db_engine.execute_query(query)
    return preprocess_data(raw_data)


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    TARGET_COLUMN = 'temperature_2m'
    FEATURES = ['season', 'period_of_day', 'hour_of_day', 'precipitation_past_3h_sum',
        'relative_humidity_past_1h', 'temperature_past_1h']
    df['date'] = pd.to_datetime(df['date'])

    # Add season for Paris
    def get_season(month):
        if month in [12, 1, 2]:
            return 0
        elif month in [3, 4, 5]:
            return 2
        elif month in [6, 7, 8]:
            return 3
        else:
            return 1

    df['season'] = df['date'].dt.month.map(get_season)

    # Add period of day
    def get_period_of_day(hour):
        if 5 <= hour < 12:
            return 1
        elif 12 <= hour < 17:
            return 3
        elif 17 <= hour < 21:
            return 2
        else:
            return 0

    df['period_of_day'] = df['date'].dt.hour.map(get_period_of_day)
    df['hour_of_day'] = df['date'].dt.hour

    # Add sum of precipitation on the past 3 hours
    df['precipitation_past_3h_sum'] = df['precipitation'].shift(1).fillna(0).rolling(window=4, min_periods=1).sum()
    df['relative_humidity_past_1h'] = df['relative_humidity_2m'].shift(1).fillna(df['relative_humidity_2m'][0])
    df['temperature_past_1h'] = df['temperature_2m'].shift(1).fillna(df['relative_humidity_2m'][0])

    scalers = open_joblib_s3(
        s3_bucket=get_env_variable('S3_BUCKET_NAME'),
        s3_key=get_env_variable('S3_SCALER_KEY')
    )

    df_scaled = np.array([
        scalers.transform(df[FEATURES + [TARGET_COLUMN]])
    ])

    return df_scaled


def save_predictions_to_db(predictions):
    current_date = datetime.datetime.now()\
        .replace(minute=0, second=0, microsecond=0)\
        .strftime('%Y-%m-%d %H:%M:%S')

    insert_query = f"""
        INSERT INTO weather_predictions (date, temperature_2m, relative_humidity_2m, precipitation, prediction) \
            VALUES ('{current_date}+00:00', -1000, -1000, -1000, {predictions[0]})
    """
    db_engine.execute_query(insert_query)


def predict_weather():
    model = open_joblib_s3(
        s3_bucket=get_env_variable('S3_BUCKET_NAME'),
        s3_key=get_env_variable('S3_MODEL_KEY')
    )

    data = get_predict_data(data)
    
    try:
        predictions = model.predict(data)
    except Exception as e:
        print(f"Error making predictions: {e}")
        raise

    save_predictions_to_db(predictions)


if __name__ == '__main__':
    predict_weather()