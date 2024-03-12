# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GemBidsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Bid_No=scrapy.Field()
    Ra_No=scrapy.Field()
    Items=scrapy.Field()
    Quantity=scrapy.Field()
    Department=scrapy.Field()
    Start_date=scrapy.Field()
    End_date=scrapy.Field()
    doclink=scrapy.Field()
