import pandas as pd
import numpy as np
from clickhouse_driver import Client
import uuid

N = 5_000_000
cities= ['Москва', 'Новосибирск', 'Тула', 'Екатеринбург', 'Казань', 
          'Санкт-Петербург']

rng = np.random.default_rng()
dates = pd.date_range('2025-01-01', '2025-12-31')

dataf = pd.DataFrame({
    'date' : pd.to_datetime(rng.choice(dates, N)).strftime('%Y-%m-%d'),
    'event': rng.choice(['view', 'purchase', 'add_to_cart'], N),
    'device_id': [str(uuid.uuid4()) for _ in range(N)],
    'city': rng.choice(cities, N),
    'device_os': rng.choice(['Android', 'iOS'], N, p=[0.5, 0.5])
})

dataf['event_time'] = pd.to_datetime(dataf['date']) + pd.to_timedelta(rng.random(N) * 86400, unit='s')

print(dataf.head())

client = Client('localhost', port=9000)

client.insert_dataframe('INSERT INTO priemniki VALUES', dataf)

dataf['date'] = pd.to_datetime(dataf['date']).dt.date
dataf['event_time'] = pd.to_datetime(dataf['event_time'])

client.insert_dataframe('INSERT INTO priemniki VALUES', dataf)

client.disconnect()

