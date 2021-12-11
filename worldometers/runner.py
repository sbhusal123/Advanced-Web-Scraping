"""
Standalone executor
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from worldometers.spiders.countries import CountriesSpider

# Get settings from settings.py file and assign
process = CrawlerProcess(settings=get_project_settings())
# process.crawl(spider, input='inputargument', first='James', last='Bond') #example showing how to pass params


process.crawl(CountriesSpider)
process.start()