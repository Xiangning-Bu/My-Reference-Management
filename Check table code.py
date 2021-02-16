import sqlite3

import pandas as pd
import numpy as np


conn = sqlite3.connect("MyRefs.db")
c = conn.cursor()

c.execute("SELECT * FROM COVID19")

# print(c.fetchone())
# print(c.fetchmany(3))

# print(c.fetchall())
df = pd.read_sql_query("SELECT * FROM COVID19", conn)
df.to_csv("covid19.csv", index=False)

print(df.head())

conn.commit()
conn.close()