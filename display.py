import pandas as pd
import sqlalchemy

with open('connection.txt', 'r') as c:
    connection_text = c.read()

engine = sqlalchemy.create_engine(connection_text)
conn = engine.connect()
df = pd.read_sql('sensor_readings', con=conn)
