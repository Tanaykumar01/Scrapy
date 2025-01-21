import scrapy
from ..items import QuoteItem
class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/'
    ]
    
    def parse(self, response):
        
        items = QuoteItem()
        
        all_quote = response.css('div.quote')
        for quote in all_quote:
            items['title'] = quote.css('span.text::text').extract()
            items['author'] = quote.css('span small.author::text').extract()
            items['tags'] = quote.css('div.tags a.tag::text').extract()
            yield items