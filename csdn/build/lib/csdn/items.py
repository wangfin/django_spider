# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class CsdnItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    blog_title = Field()
    blog_author  = Field()
    blog_time = Field()
    blog_content = Field()
    blog_viewnum = Field()
    blog_comment = Field()
    blog_url = Field()
    blog_picture = Field()

    pass
