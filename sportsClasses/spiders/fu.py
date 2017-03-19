# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from . import sportsSpider


class FuSpider(CrawlSpider):
    name = "fu"
    allowed_domains = ["www.buchsys.de"]
    start_urls = (
        'http://www.buchsys.de/fu-berlin/angebote/aktueller_zeitraum/index.html',
    )

    rules = [Rule(LinkExtractor(allow=['_.+\.html']), callback='parseDetails')]

    def parseDetails(self, response):
        return sportsSpider.parse_details(self, response)
