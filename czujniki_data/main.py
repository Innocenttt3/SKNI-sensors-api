import os
import psycopg2
import random
import json
from datetime import datetime
import time

def generate_random_weather_data(sensor_id):
    temperature_range = (-10, 20)
    humidity_range = (30, 60)
    pressure_range = (975, 1035)
    gas_resistance_range = (50, 1000)

    temperature = random.randint(*temperature_range)
    humidity = random.randint(*humidity_range)
    pressure = random.randint(*pressure_range)
    gas_resistance = random.randint(*gas_resistance_range)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    weather_data = {
        "sensor_id": sensor_id,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "timestamp": timestamp,
        "gas_resistance": gas_resistance,
    }

    return json.dumps(weather_data)

def insert_weather_data(data_json, schema_name, table_name, cur, conn):
    data = json.loads(data_json)
    query = f"""
        INSERT INTO {schema_name}.{table_name} (sensor_id, temperature, humidity, pressure, timestamp, gas_resistance)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(query, (data["sensor_id"], data["temperature"], data["humidity"], data["pressure"], data["timestamp"], data["gas_resistance"]))
    conn.commit()
    print(f"Inserted data: {data}")

def main_loop(interval):
    conn = psycopg2.connect(
        dbname="kgspring",
        user="kamil.golawski",
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port="5432"
    )
    cur = conn.cursor()
    schema_name = "weathergrid"
    table_name = "sensor_data"

    try:
        while True:
            for sensor_id in range(2, 6):
                weather_data_json = generate_random_weather_data(sensor_id)
                insert_weather_data(weather_data_json, schema_name, table_name, cur, conn)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    finally:
        cur.close()
        conn.close()
        print("Database connection closed.")

main_loop(60)