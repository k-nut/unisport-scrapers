# -*- coding: utf-8 -*-
import re

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sportsClasses.items import SportsClassItem, CourseItem, LocationItem


class TuSpider(CrawlSpider):
    name = "tu"
    allowed_domains = ["www.tu-sport.de"]
    start_urls = ['http://www.tu-sport.de/index.php?id=2472']
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
        for row in response.xpath("//tbody/tr"):
            place_url = row.css("td:nth-child(7) a::attr('href')").extract_first()
            place = row.xpath("./td[7]/descendant::*/text()").extract()
            print(place, len(place))
            if len(place) > 0:
                place_name = row.xpath("./td[7]/descendant::*/text()").extract_first()
            else:
                place_name = row.xpath("./td[7]/text()").extract_first()

            # TODO: Sometimes there are multiple classes in one row (denoted by the class addex).
            # Those should inherit the previous base properties and be extended here
            bookable = row.xpath("./td[10]/*/text()").extract_first()
            course = CourseItem(
                name=" ".join([p.strip() for p in row.xpath("./td[2]/*/text()").extract()]),
                day=row.xpath("./td[5]/abbr/text()").extract_first(),
                sports_class_url=sportsClass["url"],
                time=row.xpath("./td[6]/text()").extract_first(),
                timeframe=row.xpath("./td[4]/text()").extract_first(),
                price=row.xpath("./td[9]/abbr/text()").extract_first(),
                bookable=bookable.strip() if bookable else None,
                place=place_name,
            )

            yield course
            yield Request(response.urljoin(place_url), self.parse_location)


    def parse_location(self, response):
        osm_link = response.css(".contentstyle.twocol > a::attr('href')").extract_first()
        name = response.css("h1::text").extract_first()
        match = re.search('mlat=(.*)&mlon=(.*)&', osm_link)
        lat, lon = float(match.group(1)), float(match.group(2))
        yield LocationItem(lat=lat, lon=lon, name=name)
