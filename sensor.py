import time
import os
import board
import busio
import adafruit_scd30
import pandas as pd
import sqlalchemy


def main():
    # SCD-30 has temperamental I2C with clock stretching, datasheet recommends
    # starting at 50KHz
    i2c = busio.I2C(board.SCL, board.SDA, frequency=50_000)
    scd = adafruit_scd30.SCD30(i2c)
    with open('connection.txt', 'r') as c:
        connection_text = c.read()
    engine = sqlalchemy.create_engine(connection_text)
    conn = engine.connect()
    while True:
        if scd.data_available:
            # take advantage of pandas' built-in sql loading
            data = pd.DataFrame(
                [[pd.to_datetime('today'), scd.CO2, scd.temperature, scd.relative_humidity]],
                columns=['tstamp', 'co2', 'temperature', 'humidity'])
            data['tstamp'] = pd.to_datetime(data['tstamp'])
            data.to_sql('sensor_readings', con=conn, if_exists='append', index=False)
            print(f'Uploaded reading with co2={scd.CO2} temperature={scd.temperature} relative_humidity={scd.relative_humidity}')
        time.sleep(30)


if __name__ == '__main__':
    main()
