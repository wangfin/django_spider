# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class CategoriesItem(Item):
    name = Field()
    url = Field()
    _id = Field()
    pass


class productsItem(Item):
    product_name =  Field()
    product_url = Field()
    product_id = Field()
    reallyPrice = Field()
    originalPrice =  Field()
    favourableDesc1 = Field()
    AllCount = Field()
    GoodCount = Field()
    AfterCount = Field()
    GeneralCount = Field()
    PoorCount = Field()

class CsdnblogcrawlspiderItem(Item):
    blog_name = Field()
    blog_url = Field()



