# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']

    """
    Rules: https://docs.scrapy.org/en/2.3/topics/spiders.html#crawling-rules
    """
    rules = (
        # follows the link / path containing regular expression and handled in parse_item method
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),

        # follow except the path/link regular expression in the deny arg
        # Rule(LinkExtractor(deny=r'Items/'), callback='parse_item', follow=True),

        
        Rule(LinkExtractor(restrict_xpaths='//h3[@class="lister-item-header"]/a'), callback='parse_item', follow=True), 
        Rule(LinkExtractor(restrict_xpaths='(//a[contains(text(), "Next")])[1]')) #pagination
        # Rule(LinkExtractor(restrict_css=('.class1', '#id1')), callback='parse_item', follow=True), 
    )

    def parse_item(self, response):
        title = response.xpath('//h1[@data-testid="hero-title-block__title"]/text()').get()
        year = response.xpath('//span[contains(@class,"TitleBlockMetaData__ListItemText")]/text()').get()

        duration_text = response.xpath('//span[contains(@class,"TitleBlockMetaData__ListItemText")]/ancestor::ul/li[2]/text()').getall()
        if not duration_text:
            duration_text = response.xpath('//span[contains(@class,"TitleBlockMetaData__ListItemText")]/ancestor::ul/li[3]/text()').getall()
        duration = ''.join(t for t in duration_text)

        genre = response.xpath('//div[contains(@class, "ipc-chip-list GenresAndPlot")]/a/span/text()').getall()

        rating = response.xpath('(//div[@data-testid="hero-rating-bar__aggregate-rating__score"])[2]/span[1]/text()').get()
        movie_url = response.url
        yield {
            'title': title,
            'year': year,
            'duration': duration,
            'genre': genre,
            'rating': rating,
            'movie_url': movie_url
        }
