# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from . import sportsSpider


class HtwSpider(CrawlSpider):
    name = "htw"
    allowed_domains = ["sport.htw-berlin.de"]
    start_urls = (
        'http://sport.htw-berlin.de/angebote/aktueller_zeitraum/index.html',
    )

    rules = [Rule(LinkExtractor(allow=['_.+\.html']), callback='parseDetails')]

    def parseDetails(self, response):
        return sportsSpider.parse_details(self, response)
