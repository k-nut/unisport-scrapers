# -*- coding: utf-8 -*-
from scrapy.selector import HtmlXPathSelector
from sportsClasses.items import SportsClassItem


def parse_details(self, response):
    sports_class = SportsClassItem()
    sports_class['url'] = response.url
    sports_class['name'] = response.xpath("//div[@class='bs_head']/text()").extract_first().strip()
    sports_class['description'] = "\n".join(response.css(".bs_kursbeschreibung > p::text").extract())
    hxs = HtmlXPathSelector(response)
    tables = hxs.select("//table[@class='bs_kurse']/tbody/tr")
    dates = []
    for row in tables:
        date = {}

        date["name"] = row.xpath("./td[2]/text()").extract_first(default="Keine Angaben")

        date["day"] = row.xpath("./td[3]/text()").extract_first(default="Keine Angaben")

        date["time"] = row.xpath("./td[4]/text()").extract_first(default="Keine Angaben")

        date["place"] = row.xpath("./td[5]/a/text()").extract_first(default="Keine Angaben")

        date["timeframe"] = row.xpath("./td[6]/a/text()").extract_first()

        price_list = row.select("./td[8]/div/text()").extract()
        if len(price_list) < 1:
            price_list = row.select("./td[8]/text()").extract()
        date['price'] = price_list[0]

        bookable_list = row.xpath("./td[9]/input/@value")
        if len(bookable_list) > 0:
            date["bookable"] = row.xpath("./td[9]/input/@value")[0].extract()
        else:
            date["bookable"] = row.xpath("./td[9]/span/text()").extract_first()

        dates.append(date)

        sports_class['dates'] = dates
    return sports_class
