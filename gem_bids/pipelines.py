# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GemBidsPipeline:
    def __init__(self):
        hostname = 'localhost'
        username = 'postgres'
        password = 'admin' # your password
        database = 'test'
        self.con = psycopg2.connect(hostname=hostname, user=username, password=password, dbname=database)
        self.cur = self.con.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS bids(
                id serial PRIMARY KEY,
                Bid_No text,
                Ra_No text,
                Items int,
                Quantity int,
                Department text,
                Start_date date,
                End_date date,
                doclink text,
                )""")

    def process_item(self, items, spider):
        for item in items:
            self.cur.execute(""" 
            INSERT INTO bids (Bid_No, Ra_No, Items, Quantity, Department, Start_date, End_date, doclink) values (%s, %s, %s, %s, %s, %s, %s, %s)""", (
                item["Bid_No"],
                item["Ra_No"],
                item["Items"],
                item["Quantity"],
                item["Department"],
                item["Start_date"],
                item["End_date"],
                item["doclink"],
            ))
            self.con.commit()
        return items

    def close_spider(self):
        self.cur.close()
        self.con.close()

