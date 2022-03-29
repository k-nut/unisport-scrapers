# -*- coding: utf-8 -*-
import re

from scrapy import Request
from scrapy.shell  import inspect_response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sportsClasses.items import SportsClassItem, CourseItem, LocationItem

def safe_strip(string):
    if not string:
        return
    return string.strip()

class TuSpider(CrawlSpider):
    name = "tu"
    allowed_domains = ["www.tu-sport.de"]
    start_urls = ['https://www.tu-sport.de/sportprogramm/a-z/']
    rules = [
        Rule(LinkExtractor(allow=['sportprogramm/kurse/*']), callback='parse_details')
    ]

    def parse_details(self, response):
        if u'Im Wintersemester sind keine' in response.text:
            return

        if u'Derzeit keine Angebote vorhanden.' in response.text:
            return

        sportsClass = SportsClassItem()
        sportsClass['url'] = response.url
        sportsClass['name'] = response.xpath("//h1/text()").extract_first().strip()
        sportsClass['description'] = "".join(
            [part.strip() for part in response.css("div[role='main'] .col-xxl-9 ::text").extract()[1:]])
        yield sportsClass

        for row in response.css(".table-body-group .table-row"):
            course = self._parse_full_course_row(response, row)

            course["sports_class_url"] = sportsClass["url"]

            yield course
            yield Request(course["place_url"], self.parse_location)

    def parse_location(self, response):
        osm_link = response.css(".dwzeh > .row a::attr('href')").extract_first()
        name = response.css("h1::text").extract_first()
        if not osm_link or not name:
            return
        match = re.search('mlat=(.*)&mlon=(.*)&', osm_link)
        lat, lon = float(match.group(1)), float(match.group(2))
        yield LocationItem(lat=lat, lon=lon, name=name, url=response.url)


    def _get_column_value(self, row, column):
        return safe_strip(row.css(f'.column-{column} :not(.tablelable)::text').extract_first())

    def _parse_full_course_row(self, response, row):
        place_link = row.css(".column-6 a")
        place_url = place_link.css("::attr(href)").extract_first()
        place_name = safe_strip(place_link.css("::text").extract_first())
        full_place_url = response.urljoin(place_url)

        course = CourseItem(
            name=self._get_column_value(row, 2),
            day=self._get_column_value(row, 4),
            time=self._get_column_value(row, 5),
            timeframe=self._get_column_value(row, 3),
            price=self._get_column_value(row, 8),
            bookable=self._get_column_value(row, 9),
            place=place_name,
            place_url=full_place_url,
        )
        return course
