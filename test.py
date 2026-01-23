import pandas as pd
import numpy as np
from clickhouse_driver import Client
import uuid

N = 5_000_000
cities = ['Москва', 'Новосибирск', 'Тула', 'Екатеринбург', 'Казань', 'Санкт-Петербург']
rng = np.random.default_rng()
dates = pd.date_range('2025-01-01', '2025-12-31')

def generation(cities, dates, rng, N):
    print('Генерация')
    
    raw_dates = rng.choice(dates, N)
    
    dataf = pd.DataFrame({
        'date': raw_dates,  
        'event': rng.choice(['view', 'purchase', 'add_to_cart'], N),
        'device_id': [str(uuid.uuid4()) for _ in range(N)],
        'city': rng.choice(cities, N),
        'device_os': rng.choice(['Android', 'iOS'], N)
    })
    
    time_offset = pd.to_timedelta(rng.random(N) * 86400, unit='s')
    
    dataf['event_time'] = dataf['date'] + time_offset  
    dataf['date'] = pd.to_datetime(dataf['date']).dt.date 

    print(dataf.info())
    print(dataf.head())
    
    return dataf  

def insertion(dataf, client):
    try:
        print("Вставка DataFrame")
        client.insert_dataframe('INSERT INTO test VALUES', dataf)
        print("данные загружены")
    except Exception as e:
        print("Ошибка вставки: ", e)

def database_creation(client):
    print("Создание таблицы")
    client.execute('''
        CREATE TABLE IF NOT EXISTS test (
            date Date,
            event_time DateTime,
            event String,
            device_id String,
            city String,
            device_os String
        ) ENGINE = Memory
    ''')
    print("Таблица создана")

def show_sample(client):
    rows = client.execute('SELECT * FROM test LIMIT 5')  
    print("строки из таблицы:")
    for row in rows:
        print(row)
    total = client.execute('SELECT count() FROM test')
    print(" Всего строк: ", total)

def main():
    dataf = generation(cities, dates, rng, N)  
    
    with Client('localhost',
                user='default',
                password='',
                database='default',
                port=9000,
                settings={'use_numpy': True, 'connect_timeout': 30}) as client:
        database_creation(client)
        insertion(dataf, client)  
        show_sample(client)

if __name__ == "__main__":
    main()





