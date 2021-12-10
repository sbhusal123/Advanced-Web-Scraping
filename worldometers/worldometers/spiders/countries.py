import scrapy
import logging

class CountriesSpider(scrapy.Spider):
    name = 'countries'

    # all the domains this spider is allowed to access, no need to add protocol
    allowed_domains = ['www.worldometers.info']

    # starts crawling the site from url below.
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        """Initial response is passed to this method by default"""
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # Gives full url with protocal: https://xyz.com/path/to/...
            absolute_url = response.urljoin(link)

            """
                # make sure allowed_domains has no slash '/'
                yield response.follow(url=link)
            """
            yield scrapy.Request(url=absolute_url, callback=self.parse_country)

    def parse_country(self, response):
        """Crawl country page"""
        rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')

        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield {
                'year': year,
                'population': population
            }
