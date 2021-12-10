# -*- coding: utf-8 -*-
import scrapy


class SpecialOfferSpider(scrapy.Spider):
    name = 'special_offer'
    allowed_domains = ['www.cigabuy.com']
    start_urls = ['https://www.cigabuy.com/specials.html']

    def parse(self, response):
        for product in response.xpath('//div[@class="p_box_wrapper"]'):
            yield {
                'title': product.xpath('.//a[@class="p_box_title"]/text()').get(),
                'url': product.xpath('.//a[@class="p_box_title"]/@href').get(),
                'discounted_price': product.xpath('.//span[@class="productSpecialPrice fl"]/text()').get(),
                'original_price': product.xpath('.//span[@class="normalprice fl"]/text()').get(),
            }
