from .sports_spider import SportsSpider


class BeuthSpider(SportsSpider):
    name = "beuth"
    allowed_domains = ["zeh02.bht-berlin.de"]
    start_urls = (
        'https://zeh02.bht-berlin.de/angebote/aktueller_zeitraum/index.html',
    )

