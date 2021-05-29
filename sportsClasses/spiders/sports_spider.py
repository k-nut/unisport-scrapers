# -*- coding: utf-8 -*-
import json
import re
from collections import namedtuple
from urllib.parse import urljoin
import html

from scrapy.spiders import CrawlSpider, Rule
from scrapy.shell import inspect_response
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

    def inner_text(self, row, selector: str) -> str:
        return " ".join(row.xpath(selector).css('::text').extract())

    def parse_details(self, response):
        sports_class = SportsClassItem()
        sports_class['url'] = response.url
        sports_class['name'] = response.xpath("//div[@class='bs_head']/text()").extract_first().strip()
        sports_class['description'] = "\n".join(response.css(".bs_kursbeschreibung > p::text").extract())
        yield sports_class

        for row in response.xpath("//table[@class='bs_kurse']/tbody/tr"):
            place_link = row.xpath("./td[5]/a")
            place = self.inner_text(place_link, ".")
            place_url = place_link.css("::attr(href)").extract_first()
            course = CourseItem(
                name=self.inner_text(row, "./td[2]"),
                day=self.inner_text(row, "./td[3]"),
                time=self.inner_text(row, "./td[4]"),
                place=place,
                place_url=response.urljoin(place_url),
                timeframe=self.inner_text(row, "./td[6]/a"),
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
        location_links = response.css('.bs_flmenu li a')
        urls_by_name = { }
        for link in location_links:
            url = link.css("::attr(href)").extract_first()
            name = link.css(".bs_spname::text").extract_first()
            urls_by_name[name] = response.urljoin(url)

        match = re.search('.*var markers=(.*)', response.text)
        js_list = match.group(1)
        # the line ends with a semicolon. Strip it before parsing
        locations = json.loads(js_list[:-1])
        for location in locations:
            name = html.unescape(location[2])
            url = urls_by_name.get(name)
            yield LocationItem(lat=location[0], lon=location[1], name=name, url=url)
