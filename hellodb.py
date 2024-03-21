import psycopg2

con = psycopg2.connect(
        host="localhost", # summerking? 
        database="test", 
        user="postgres",
        password="admin",
        port="5432"
    )

cur = con.cursor()
cur.execute("SELECT * FROM testtable")
row = cur.fetchall()

print(row)
# for r in rows:

cur.close()
con.close()
