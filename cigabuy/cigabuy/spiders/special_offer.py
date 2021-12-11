# -*- coding: utf-8 -*-
import scrapy


class SpecialOfferSpider(scrapy.Spider):
    name = 'special_offer'
    allowed_domains = ['www.cigabuy.com']
    # start_urls = ['https://www.cigabuy.com/specials.html']

    def start_requests(self):
        """
            Start request with different user agent:
            - No need to specify starts_url if this method is overriden
            - Only the first request will be using the defined user  agent.
        """
        yield scrapy.Request(url="https://www.cigabuy.com/specials.html", callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
        })

    def parse(self, response):
        for product in response.xpath('//div[@class="p_box_wrapper"]'):
            yield {
                'title': product.xpath('.//a[@class="p_box_title"]/text()').get(),
                'url': product.xpath('.//a[@class="p_box_title"]/@href').get(),
                'discounted_price': product.xpath('.//span[@class="productSpecialPrice fl"]/text()').get(),
                'original_price': product.xpath('.//span[@class="normalprice fl"]/text()').get(),
                'User-Agent': response.request.headers['User-Agent']
            }

        next_url = response.xpath('(//a[@class="nextPage"])[2]/@href').get()
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
            })
