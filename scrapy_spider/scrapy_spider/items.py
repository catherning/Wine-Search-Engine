# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Wine(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    score = scrapy.Field()
    vintage = scrapy.Field()
    type_wine = scrapy.Field()
    variety = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    winerie = scrapy.Field()

class Winerie(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    country = scrapy.Field()
    variety = scrapy.Field()
    wines = scrapy.Field() # put the list of wines ?

class Country(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()

class Region(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    country = scrapy.Field()