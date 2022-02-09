import scrapy
from ..items import BookstoreItem

class BookInfoSpider(scrapy.Spider):
    name = 'book_info'
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
        book_selectors = response.xpath("//article")
        for book_selector in book_selectors:
            self.index += 1
            index = self.index

            book = BookstoreItem()
            book['index']=index
            book['name']=book_selector.xpath("h3/a/@title").get()
            book['price']=book_selector.xpath("div[2]/p[1]/text()").get()
            book['rating']=book_selector.xpath("p/@class").get().split()[1]
            book['stock']="In stock" in ''.join(book_selector.xpath("div[2]/p[2]/text()").getall())

            book_page = book_selector.xpath("h3").css("a::attr(href)").get()
            book_page = response.urljoin(book_page)
            request = scrapy.Request(book_page, self.parse_genre, cb_kwargs=book)

            yield request

        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)

    def parse_genre(self, response, index, name, price, rating, stock):
        genre = response.xpath("//ul/li[3]/a/text()").get()
        UPC = response.xpath("//tr[1]/td/text()").get()

        book = BookstoreItem()
        book['index'] = index
        book['name'] = name
        book['price'] = price
        book['rating'] = rating
        book['stock'] = stock
        book['genre'] = genre
        book['UPC'] = UPC
        yield book