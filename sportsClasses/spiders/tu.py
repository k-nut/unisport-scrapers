# -*- coding: utf-8 -*-
import re

from scrapy import Request
from scrapy.shell  import inspect_response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sportsClasses.items import SportsClassItem, CourseItem, LocationItem


class TuSpider(CrawlSpider):
    name = "tu"
    allowed_domains = ["www.tu-sport.de"]
    start_urls = ['https://www.tu-sport.de/index.php?id=2472']
    rules = [
        Rule(LinkExtractor(allow=['index.php\?id=2860.*']), callback='parse_details')
    ]

    def parse_details(self, response):
        if u'Im Wintersemester sind keine' in response.body_as_unicode():
            return

        if u'Derzeit keine Angebote vorhanden.' in response.body_as_unicode():
            return

        sportsClass = SportsClassItem()
        sportsClass['url'] = response.url
        sportsClass['name'] = response.xpath("//h1/text()").extract_first().strip()
        sportsClass['description'] = "".join(
            [part.strip() for part in response.xpath("//div[@class='contentstyle twocol']/*/text()").extract()[1:]])
        yield sportsClass

        prev = None
        for row in response.xpath("//tbody/tr"):
            if "addex" in row.attrib.get('class', ""):
                addex_course = self._parse_addex_course_row(response, row)
                # This should create a new item that takes all the values
                # from the previous row and overrides the updated ones
                # from the new row
                course = CourseItem(**{**prev, **addex_course})
            else:
                course = self._parse_full_course_row(response, row)

            course["sports_class_url"] = sportsClass["url"]
            prev = course

            yield course
            yield Request(course["place_url"], self.parse_location)


    def parse_location(self, response):
        osm_link = response.css(".contentstyle.twocol > a::attr('href')").extract_first()
        name = response.css("h1::text").extract_first()
        match = re.search('mlat=(.*)&mlon=(.*)&', osm_link)
        lat, lon = float(match.group(1)), float(match.group(2))
        yield LocationItem(lat=lat, lon=lon, name=name, url=response.url)

    def _parse_addex_course_row(self, response, row):
        place_link = row.css("td:nth-child(3) a")
        place_url = place_link.css("::attr(href)").extract_first()
        place_name = place_link.css("::text").extract_first()
        full_place_url = response.urljoin(place_url)
        course = CourseItem(
            day=row.css("td:nth-child(1) abbr::text").extract_first(),
            time=row.xpath("./td[2]/text()").extract_first(),
            place=place_name,
            place_url=full_place_url,
        )
        return course

    def _parse_full_course_row(self, response, row):
        place_link = row.css("td:nth-child(7) a")
        place_url = place_link.css("::attr(href)").extract_first()
        place_name = place_link.css("::text").extract_first()
        full_place_url = response.urljoin(place_url)

        # Some items use an abbreviation in their content (e.g. A-F),
        # Some just contain a direct value (e.g. Ligatraining ab F2)
        name_abbreviated = row.css('td:nth-child(2) abbr::text').extract_first()
        name_full = row.css('td:nth-child(2)::text').extract_first()

        bookable = row.xpath("./td[10]/*/text()").extract_first()
        course = CourseItem(
            name=name_abbreviated or name_full,
            day=row.css("td:nth-child(5) abbr::text").extract_first(),
            time=row.xpath("./td[6]/text()").extract_first(),
            timeframe=row.xpath("./td[4]/text()").extract_first(),
            price=row.xpath("./td[9]/abbr/text()").extract_first(),
            bookable=bookable.strip() if bookable else None,
            place=place_name,
            place_url=full_place_url,
        )
        return course
