# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImgItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img_url = scrapy.Field()
    img_website = scrapy.Field()
    img_name = scrapy.Field()
    img_path = scrapy.Field()

class MvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    keyword = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    rename = scrapy.Field()
