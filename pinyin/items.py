# -*- coding: utf-8 -*-

import scrapy


class PinyinItem(scrapy.Item):
    word = scrapy.Field()
    pinyin = scrapy.Field()
    full_letters = scrapy.Field()
    first_letters = scrapy.Field()
