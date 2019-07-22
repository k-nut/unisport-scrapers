# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from . import sportsSpider


class PostdamSpider(CrawlSpider):
    name = "potsdam"
    allowed_domains = ["buchung.hochschulsport-potsdam.de"]
    start_urls = (
        'https://buchung.hochschulsport-potsdam.de/angebote/aktueller_zeitraum/index.html',
    )

    rules = [Rule(LinkExtractor(allow=['_.+\.html']), callback='parseDetails')]

    def parseDetails(self, response):
        return sportsSpider.parse_details(self, response)
