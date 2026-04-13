from .sports_spider import SportsSpider


class FuSpider(SportsSpider):
    name = "fu"
    allowed_domains = ["www.fu-sport.de"]
    start_urls = (
        'https://www.fu-sport.de/angebote/aktueller_zeitraum/index.html',
    )
