# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class TaobaoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    url = Field()


    pass

class DetailCategoryItem(Item):
    url = Field()
    name = Field()

class TaobaoProductItem(Item):
    product_name = Field()
    product_url = Field()
    product_id = Field()
    Price = Field()
    ActualPrice = Field()
    # favourableDesc1 = Field()
    AllCount = Field()
    GoodCount = Field()
    AfterCount = Field()
    GeneralCount = Field()
    PoorCount = Field()
    sellerlink = Field()
    sellerNick = Field()


class TmallProductItem(Item):
    product_name = Field()
    product_url = Field()
    product_id = Field()
    defaultPrice = Field()
    num = Field()
    Price = Field()
    seller_link = Field()
    CommentCount = Field()
    sellerName = Field()