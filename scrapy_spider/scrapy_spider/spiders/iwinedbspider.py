import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_spider.items import Wine

import re
import csv #TODO remove later ?

class iwinedbSpider(CrawlSpider):
    name = 'iWineDB'

    allowed_domain=['http://iwinedb.com']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=(r'WineriesBrowseGeo*',r'WineryDetails*' ),deny=(r"twitter",r'facebook'))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=(r'WineDetails*', ),deny=(r"twitter",r'facebook')), callback='parse_wine'),
    )

    def start_requests(self):
        urls = ['http://iwinedb.com/Wineries.aspx']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # def parse_countries(self, response):
    #     pass

    #     # countries = response.css('a[href^=Wineries] ::text').getall()
    #     # countries_page = response.css('a[href^=Wineries]::attr(href)').getall()

    #     # with open("countries.csv", 'w',newline="") as f:
    #     #     wr = csv.writer(f)
    #     #     for i in range(len(countries)):
    #     #         wr.writerow([countries[i],countries_page[i]])

    #     # self.log('Saved files.')

    #     country = items.Country()
    #     country["name"]=response.css('td[id=TableCellBreadCrumb] a::text').extract()[3]
    #     country['url']=response.url

    #     return country

    # def parse_region(self, response):
    #     pass


    # def parse_wineries(self, response):
    #     pass

    def parse_wine(self, response):
        wine = Wine()
        wine["name"]=response.xpath("//span[@id='LabelWineTitle']//text() ").extract_first()
        wine[" url"] = response.url
        wine["price"]=response.xpath("//span[@id='LabelReleasePrice']//text() ").extract_first() #XXX price keep currency!!!! (so also in database from winemag, TODO add currency and change type of column)
        
        wine["vintage"]=response.xpath("//span[@id='LabelVintage']//text() ").extract_first()
        wine["type_wine"]=response.xpath("//span[@id='LabelVarietalType']//text() ").extract_first()
        wine["variety"]=response.xpath("//span[@id='LabelVarietal']//text() ").extract_first()
        wine["country"]=response.css('td[id=TableCellBreadCrumb] a::text').extract()[3]
        wine["region"] = response.css('td[id=TableCellBreadCrumb] a::text').extract()[4:-1] #TODO check

        # wine["score"] # average of the scores
        scores=response.css('td[class="DataCell"]::text').extract()
        scores=[int(el) for el in scores if not re.search(r'\D',el)]
        average=0
        for i,score in scores:
            if i%2==1:
                average+=score
        wine["score"]= average*2/len(scores)
        #XXX might give error if no rating ?

        wine["winerie"] =response.css('td[id=TableCellBreadCrumb] a::text').extract()[-1]

        print("Found a wine.")
        return wine