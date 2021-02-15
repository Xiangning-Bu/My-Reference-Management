import sqlite3

conn = sqlite3.connect("MyRefs.db")
c = conn.cursor()


c.execute("SELECT * FROM COVID19")

# print(c.fetchone())
print(c.fetchmany(3))

# print(c.fetchall())
conn.commit()
conn.close()