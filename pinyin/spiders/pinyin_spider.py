# -*- coding: utf-8 -*-

import re
import scrapy
from pinyin.items import PinyinItem


class PinyinSpider(scrapy.Spider):
    name = 'pinyin'

    def start_requests(self):
        with open('words.txt') as f:
            words = f.readlines()

        for word in words:
            url = 'http://dict.youdao.com/w/%s' % word
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        item = PinyinItem()
        item['word'] = response.css('.keyword::text').extract_first()
        item['pinyin'] = response.css('.phonetic::text').re_first(r'\[([^]]+)\]')

        item['full_letters'] = item['pinyin']
        patterns = [(u'āáǎà', 'a'), (u'ōóǒò', 'o'), (u'ēéěè', 'e'), (u'īíǐì', 'i'), (u'ūúǔù', 'u'), (u'ǖǘǚǜ', 'v')]
        for pattern, replacement in patterns:
            for letter in pattern:
                item['full_letters'] = item['full_letters'].replace(letter, replacement)

        item['first_letters'] = re.sub(r'\B\w|\s', '', item['full_letters'])
        item['full_letters'] = item['full_letters'].replace(' ', '')
        
        yield item
