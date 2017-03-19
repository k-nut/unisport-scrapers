# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from . import sportsSpider


class BeuthSpider(CrawlSpider):
    name = "beuth"
    allowed_domains = ["zeh02.beuth-hochschule.de"]
    start_urls = (
        'http://zeh02.beuth-hochschule.de/angebote/aktueller_zeitraum/index.html',
    )

    rules = [Rule(LinkExtractor(allow=['_.+\.html']), callback='parseDetails')]

    def parseDetails(self, response):
        return sportsSpider.parse_details(self, response)
