from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import Selector
import re

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('bd_search')
    process.start()