from .sports_spider import SportsSpider


class FuSpider(SportsSpider):
    name = "fu"
    allowed_domains = ["www.buchsys.de"]
    start_urls = (
        'https://www.buchsys.de/fu-berlin/angebote/aktueller_zeitraum/index.html',
    )
