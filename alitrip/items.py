# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Route(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    transfer = scrapy.Field()
    numOfTransfer = scrapy.Field() 
    price = scrapy.Field()
    flights = scrapy.Field()

class Flight(scrapy.Item):
	airLines = scrapy.Field()
	depatureTime = scrapy.Field()
	arriveTime = scrapy.Field() 
