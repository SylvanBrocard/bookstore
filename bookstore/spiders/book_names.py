import scrapy
from ..items import BookstoreItem

class BookNamesSpider(scrapy.Spider):
    name = 'book_names'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    index = 0

    def start_request(self):
        index = 0
        urls = self.start_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info("running the parser")
        names = response.xpath("//article/h3/a/@title").getall()
        for name in names:
            self.index += 1
            index = self.index
            book = BookstoreItem()
            book['index']=index
            book['name']=name

            yield book

        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)