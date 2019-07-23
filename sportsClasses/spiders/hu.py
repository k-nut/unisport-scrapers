from .sports_spider import SportsSpider


class HuSpider(SportsSpider):
    name = "hu"
    allowed_domains = ["zeh2.zeh.hu-berlin.de"]
    start_urls = (
        'http://zeh2.zeh.hu-berlin.de/sportarten/aktueller_zeitraum/index.html',
    )
