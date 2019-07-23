from .sports_spider import SportsSpider


class BeuthSpider(SportsSpider):
    name = "beuth"
    allowed_domains = ["zeh02.beuth-hochschule.de"]
    start_urls = (
        'http://zeh02.beuth-hochschule.de/angebote/aktueller_zeitraum/index.html',
    )

