# -*- coding: utf-8 -*-
import json
import re
from collections import namedtuple
from urllib.parse import urljoin
import html

from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url

from sportsClasses.items import SportsClassItem, LocationItem, CourseItem


class LocationLinkExtractor(LinkExtractor):
    def extract_links(self, response):
        base_url = get_base_url(response)
        full_url = urljoin(base_url, "../../cgi/webpage.cgi?orte")
        x = namedtuple('item', ['url', 'text'])
        x.url = full_url
        return [x]


class SportsSpider(CrawlSpider):
    rules = [
        Rule(LinkExtractor(allow=['_.+\.html']), callback='parse_details'),
        Rule(LocationLinkExtractor(allow=['_.+\.html']), callback='parse_locations')
    ]

    def parse_details(self, response):
        sports_class = SportsClassItem()
        sports_class['url'] = response.url
        sports_class['name'] = response.xpath("//div[@class='bs_head']/text()").extract_first().strip()
        sports_class['description'] = "\n".join(response.css(".bs_kursbeschreibung > p::text").extract())
        yield sports_class

        for row in response.xpath("//table[@class='bs_kurse']/tbody/tr"):
            course = CourseItem(
                name=row.xpath("./td[2]/text()").extract_first(),
                day=row.xpath("./td[3]/text()").extract_first(),
                time=row.xpath("./td[4]/text()").extract_first(),
                place=row.xpath("./td[5]/a/text()").extract_first(),
                timeframe=row.xpath("./td[6]/a/text()").extract_first(),
                price=row.xpath("./td[8]//text()").extract_first(),
            )

            bookable_list = row.xpath("./td[9]/input/@value")
            if len(bookable_list) > 0:
                course['bookable'] = row.xpath("./td[9]/input/@value")[0].extract()
            else:
                course['bookable'] = row.xpath("./td[9]/span/text()").extract_first()

            course['sports_class_url'] = sports_class['url']
            yield course

    def parse_locations(self, response):
        match = re.search('.*var markers=(.*)', response.body.decode('utf-8'))
        js_list = match.group(1)
        # the line ends with a semicolon. Strip it before parsing
        locations = json.loads(js_list[:-1])
        for location in locations:
            yield LocationItem(lat=location[0], lon=location[1], name=html.unescape(location[2]))
