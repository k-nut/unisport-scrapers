from .sports_spider import SportsSpider


class PostdamSpider(SportsSpider):
    name = "potsdam"
    allowed_domains = ["buchung.hochschulsport-potsdam.de"]
    start_urls = (
        'https://buchung.hochschulsport-potsdam.de/angebote/aktueller_zeitraum/index.html',
    )
