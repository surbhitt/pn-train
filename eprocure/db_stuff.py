import psycopg2

def open():
    hostname = 'localhost'
    username = 'postgres'
    password = 'admin' 
    database = 'test'
    con = psycopg2.connect(password=password, host=hostname, database=database, user=username)
    cur = con.cursor()
    return cur, con

def close(cur, con):
    cur.close()
    con.close()

def create_table():
    cur, con = open()
    cur.execute("""CREATE TABLE eproc(
            sno serial PRIMARY KEY, 
            pub_date text, 
            bid_sub_close text, 
            tend_open text, 
            title text, 
            org text, 
            link text, 
            refno text, 
            tend_type text, 
            tend_cat text, 
            fee text, 
            loc text, 
            emd text, 
            des text, 
            doc text 
        )""")
    close(cur, con)

def populate_table(item):
    cur, con = open()
    print(item)
    cur.execute("""
        INSERT INTO eproc VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, )
                """, (
            item.get("sno", ""),
            item.get("pub_date", ""),
            item.get("bid_sub_close", ""),
            item.get("tend_open", ""),
            item.get("title", ""),
            item.get("org", ""),
            item.get("link", ""),
            item.get("refno", ""),
            item.get("tend_type", ""),
            item.get("tend_cat", ""),
            item.get("fee", ""),
            item.get("loc", ""),
            item.get("emd", ""),
            item.get("des", ""),
            item.get("doc", ""))
        )
    con.commit()
    close(cur,con)


