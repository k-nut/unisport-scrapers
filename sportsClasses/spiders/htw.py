from .sports_spider import SportsSpider


class HtwSpider(SportsSpider):
    name = "htw"
    allowed_domains = ["sport.htw-berlin.de"]
    start_urls = (
        'http://sport.htw-berlin.de/angebote/aktueller_zeitraum/index.html',
    )
