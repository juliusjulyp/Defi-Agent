import cryptocompare
import pandas as pd
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')
cryptocompare.cryptocompare._set_api_key_parameter('api_key')

def fetch_historical_data(ticker, currency, start_date, end_date):
    all_data = []
    current_date = end_date

    while current_date > start_date:
        to_timestamp = int(current_date.timestamp())
        data = cryptocompare.get_historical_price_hour(ticker, currency, limit=2000, toTs=to_timestamp)
        if not data:
            break
        all_data.extend(data)
        current_date -= timedelta(hours=2000)
        time.sleep(1)  

    return all_data


ticker = "BTC"
currency = "USD"
start_date = datetime(2015, 1, 1)
end_date = datetime.now()

historical_data = fetch_historical_data(ticker, currency, start_date, end_date)


print(historical_data[:5])
df = pd.DataFrame(historical_data)


if 'time' in df.columns:
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
else:
    print("Column 'time' not found in DataFrame. Available columns are:", df.columns.tolist())
 
df.to_csv('btc_usd_hourly_data.csv')