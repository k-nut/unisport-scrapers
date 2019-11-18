# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SportsClassItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()


class CourseItem(scrapy.Item):
    sports_class_url = scrapy.Field()
    name = scrapy.Field()
    day = scrapy.Field()
    place = scrapy.Field()
    price = scrapy.Field()
    time = scrapy.Field()
    timeframe = scrapy.Field()
    bookable = scrapy.Field()
    url = scrapy.Field()


class LocationItem(scrapy.Item):
    name = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
