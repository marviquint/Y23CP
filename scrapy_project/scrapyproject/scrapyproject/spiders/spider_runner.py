import signal
signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_project.scrapyproject.scrapyproject.spiders.lawspider import MySpider
import json
from scrapy.exceptions import DropItem
from twisted.internet import reactor, defer


def run_spider(url):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    deferred = process.crawl(MySpider, start_url=url)

    def handle_results(results):
        if results is None:
            return []
        scraped_data = []
        for result in results:
            if isinstance(result, dict):
                scraped_data.append(result)

        # Write scraped data to a JSON file
        with open('results.json', 'w') as f:
            json.dump(scraped_data, f)

        # Return the path to the output file
        return 'results.json'

    def handle_error(failure):
        if failure.check(DropItem):
            print('Item dropped:', failure.value)
        else:
            print('Error:', failure.getErrorMessage())

    deferred.addCallbacks(handle_results, handle_error)
    deferred.addBoth(lambda _: reactor.stop())

    # Remove reactor.run() call
    return handle_results([])


def run_spider_async(url):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    deferred = process.crawl(MySpider, start_url=url)

    def handle_results(results):
        if results is None:
            return []
        scraped_data = []
        for result in results:
            if isinstance(result, dict):
                scraped_data.append(result)

        # Write scraped data to a JSON file
        with open('results.json', 'w') as f:
            json.dump(scraped_data, f)

        # Return the path to the output file
        return 'results.json'

    def handle_error(failure):
        if failure.check(DropItem):
            print('Item dropped:', failure.value)
        else:
            print('Error:', failure.getErrorMessage())

    deferred.addCallbacks(handle_results, handle_error)

    # Call reactor.run() to start the Twisted event loop
    reactor.run()

    # Return the Deferred object
    return deferred
