import scrapy
from scrapy.http import HtmlResponse


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    def __init__(self, search_term=None, **kwargs):
        self.search_term = search_term
        super().__init__(**kwargs)

    def start_requests(self):
        url = self.search_term
        yield scrapy.Request(url=url, callback=self.parse, errback=self.handle_error, headers={'User-Agent': self.custom_settings['USER_AGENT']})

    def parse(self, response: HtmlResponse):
        if response.status != 200:
            self.logger.error('Received non-200 response for URL: %s', response.url)
            return

        quotes = []
        for quote in response.css('div.quote'):
            quotes.append({
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            })

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse, errback=self.handle_error, headers={'User-Agent': self.custom_settings['USER_AGENT']})

        yield {
            'quotes': quotes,
            'url': response.url,
        }

    def handle_error(self, failure):
        self.logger.error('Error occurred while crawling: %s', failure)
