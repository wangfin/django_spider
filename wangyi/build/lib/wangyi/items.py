# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
#from scrapy.contrib.djangoitem import DjangoItem
#from show.models import news
class DmozItem(Item):
    """
    define the fields for your item here like.
    for crawl dmoz items
    """
    #django_model = commodity
    title = Field()
    link = Field()

class NewsItem(Item):
    """
    define the fields for news
    for crawl news items
    """
    #django_model = news
    id = Field()
    url = Field()
    source = Field()
    title = Field()
    editor = Field()
    time = Field()
    content = Field()
