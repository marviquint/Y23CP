from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy_project.scrapyproject.scrapyproject.spiders.lawspider import MySpider
import json
from scrapy.exceptions import DropItem
import os

def run_spider(url):
    spider_cls = MySpider
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(spider_cls, start_url=url)

    def handle_results(results):
        scraped_data = []
        for result in results:
            if isinstance(result, dict):
                scraped_data.append(result)

        # Write scraped data to a JSON file
        file_path = os.path.join(os.getcwd(), 'output.json')
        with open(file_path, 'w') as f:
            json.dump(scraped_data, f)

    def handle_error(failure):
        if failure.check(DropItem):
            print('Item dropped:', failure.value)
        else:
            print('Error:', failure.getErrorMessage())

    deferred.addCallbacks(handle_results, handle_error)
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()
