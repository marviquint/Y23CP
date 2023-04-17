import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")
django.setup()

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from scrapy_project.scrapyproject.scrapyproject.spiders.scrapyspider import QuotesSpider
from twisted.internet import reactor

def run_spider(url):
    scraped_data = []
    process = CrawlerProcess(get_project_settings())
    process.crawl(QuotesSpider, search_term=url, scraped_data=scraped_data)
    reactor.run(installSignalHandlers=False)
    return scraped_data