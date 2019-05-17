import scrapy

class iwinedbSpider(scrapy.Spider):
    name = 'iWineDB'
    start_urls = ['http://http://iwinedb.com/Wineries.aspx']

    def parse(self, response):
    # proceed to other pages of the listings
    for page_url in response.css('a[title ~= page]::attr(href)').extract():
        page_url = response.urljoin(page_url)
        yield scrapy.Request(url=page_url, callback=self.parse)