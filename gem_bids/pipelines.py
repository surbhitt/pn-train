# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import itemadapter
import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GemBidsPipeline:
    def __init__(self):
        host = 'localhost'
        user = 'postgres'
        passw = 'admin'
        db = 'test'
        self.con = psycopg2.connect(host=host, user=user, password=passw, database=db)
        self.cur = self.con.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS bids(
                id serial PRIMARY KEY,
                Bid_No text,
                Ra_No text,
                Items text,
                Quantity int,
                Department text,
                Start_date date,
                End_date date,
                doclink text
                )""")

    def process_item(self, item, spider):
        for k in item:
            if not item[k]:
                item[k] = "NA"
        self.cur.execute(""" 
        INSERT INTO bids (Bid_No, Ra_No, Items, Quantity, Department, Start_date, End_date, doclink) values (%s, %s, %s, %s, %s, %s, %s, %s)""", (
            item["Bid_No"][0] if len(item["Bid_No"]) else "NA",
            item["Ra_No"][0],
            item["Items"],
            item["Quantity"][0],
            item["Department"][0],
            item["Start_date"],
            item["End_date"],
            item["doclink"]
        ))
        self.con.commit()
        return item

    def close_spider(self):
        self.cur.close()
        self.con.close()

