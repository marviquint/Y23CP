import scrapy

class MySpider(scrapy.Spider):
    name = 'sapphire1_891'

    def __init__(self, start_url=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_url = start_url

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        # Extract data from the main page if needed
        # ...

        # Follow links to other pages
        links = response.css('#co_contentColumn li+ li a::attr(href)').getall()
        print("Links found: ", links)
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_link)

    def parse_link(self, response):
        # Extract data from the link page
        # ...
        # Extract title first
        rule_name = '\u000A'.join(response.css('#title').css('::text').getall())
        # Extract the rules content
        data = '\u000A'.join(response.css('#co_document').css('::text').getall())
        print("Data extracted from page: ", rule_name, data)
        
        # Store the data in an item
        item = {}
        item[''+rule_name] = data
        
        yield item
        # Follow more links if needed
        for link in response.css('#co_contentColumn li+ li a::attr(href)').getall():
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_link)
