import scrapy
import csv


class iwinedbSpider(scrapy.Spider):
    name = 'iWineDB'

    def start_requests(self):
        urls = ['http://iwinedb.com/Wineries.aspx']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        countries = response.css('a[href^=Wineries] ::text').getall()
        print(countries)
        countries_page = response.css('a[href^=Wineries]::attr(href)').getall()
        print(countries_page)

        with open("countries.csv", 'w',newline="") as f:
            wr = csv.writer(f)
            for i in range(len(countries)):
                wr.writerow([countries[i],countries_page[i]])

        self.log('Saved files.')

        # yield scrapy.Request(url=page_url, callback=self.parse)
