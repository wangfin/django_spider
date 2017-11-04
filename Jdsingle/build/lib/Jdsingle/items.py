# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class JdsingleItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_url = Field()
    product_name = Field()
    product_url = Field()
    product_id = Field()
    reallyPrice = Field()
    originalPrice = Field()
    favourableDesc1 = Field()
    AllCount = Field()
    GoodCount = Field()
    AfterCount = Field()
    GeneralCount = Field()
    PoorCount = Field()
    pass
