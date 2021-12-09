# -*- coding: utf-8 -*-
import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'

    # all the domains this spider is allowed to access, no need to add protocol
    allowed_domains = ['www.worldometers.info/']

    # starts crawling the site from url below.
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        """Initial response is passed to this method by default"""
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a/text()").getall()

        yield {
            'title': title,
            'coiuntries': countries
        }

