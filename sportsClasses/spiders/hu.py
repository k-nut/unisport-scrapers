# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from . import sportsSpider


class HuSpider(CrawlSpider):
    name = "hu"
    allowed_domains = ["zeh2.zeh.hu-berlin.de"]
    start_urls = (
        'http://zeh2.zeh.hu-berlin.de/sportarten/aktueller_zeitraum/index.html',
    )

    rules = [Rule(LinkExtractor(allow=['_.+\.html']), callback='parseDetails')]

    def parseDetails(self, response):
        return sportsSpider.parse_details(self, response)
