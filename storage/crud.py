import psycopg
import pprint
import pandas as pd

CONNINFO = "host=localhost port=5432 dbname=area_calculator user=postgres password=postgres"


with psycopg.connect(CONNINFO) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM shape")
        pprint.pprint(cur.fetchall())

    df = pd.read_sql("SELECT * FROM shape", conn)
    print(df)
