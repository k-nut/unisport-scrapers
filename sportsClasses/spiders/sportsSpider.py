# -*- coding: utf-8 -*-
from scrapy.selector import HtmlXPathSelector
from sportsClasses.items import SportsClassItem


def try_extract(row, selector):
    name_list = row.select(selector).extract()
    if name_list:
        return name_list[0]
    else:
        return 'Keine Angaben'


def parse_details(self, response):
    sports_class = SportsClassItem()
    sports_class['url'] = response.url
    sports_class['name'] = response.xpath("//div[@class='bs_head']/text()").extract_first()
    sports_class['description'] = "\n".join(response.css(".bs_kursbeschreibung > p::text").extract())
    hxs = HtmlXPathSelector(response)
    tables = hxs.select("//table[@class='bs_kurse']/tbody/tr")
    dates = []
    for row in tables:
        date = {}

        date["name"] = try_extract(row, "./td[2]/text()")

        date["day"] = try_extract(row, "./td[3]/text()")

        date["time"] = try_extract(row, "./td[4]/text()")

        date["place"] = try_extract(row, "./td[5]/a/text()")

        date["timeframe"] = row.select("./td[6]/a/text()").extract_first()

        price_list = row.select("./td[8]/div/text()").extract()
        if len(price_list) < 1:
            price_list = row.select("./td[8]/text()").extract()
        date['price'] = price_list[0]

        bookable_list = row.select("./td[9]/input/@value")
        if len(bookable_list) > 0:
            date["bookable"] = row.select("./td[9]/input/@value")[0].extract()
        else:
            date["bookable"] = row.select("./td[9]/span/text()").extract_first()

        dates.append(date)

        sports_class['dates'] = dates
    return sports_class
