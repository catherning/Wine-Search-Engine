import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_spider.items import Wine

import re
import csv #TODO remove later ?

class iwinedbSpider(CrawlSpider):
    name = 'iWineDB'

    allowed_domain=['http://iwinedb.com']

    #handle_httpstatus_list = [302]

    rules = (
        Rule(LinkExtractor(allow=(r'^WineriesBrowseGeo'),deny=(r"twitter",r'facebook')),follow=True),
        Rule(LinkExtractor(allow=(r'^WineryDetails'),deny=(r"twitter",r'facebook')), callback='parse_winerie'),
        Rule(LinkExtractor(allow=(r'^WineDetails'),deny=(r"twitter",r'facebook')), callback='parse_wine'),
        
    )

    # def __init(self):
    #     self.driver = webdriver.Chrome("D:\Documents\Tsinghua\WIR-WineSearch\chromedriver.exe")

    def start_requests(self):
        urls = ['http://iwinedb.com/Wineries.aspx']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse_winerie(self,response):
        # if response.status!=200:
        #     with open("not_processed_urls.txt","w") as f:
        #         f.write(response.url)
        
        wine_list_id=response.xpath("//td[@class='DataCell']").extract()
        wine_list_id=[re.sub(r"<(.*?)>","",x) for x in wine_list_id]
        wine_list_id=[x for i,x in enumerate(wine_list_id) if i%9==0]

        urls_list=["http://iwinedb.com/WineDetails.aspx?wid={}&p=0".format(wine_id) for wine_id in wine_list_id ]

        for url in urls_list:
            yield scrapy.Request(url=url, callback=self.parse_wine)

    def parse_wine(self, response):
        # if response.status!=200:
        #     with open("not_processed_urls.txt","a") as f:
        #             f.write(response.url+"\n")

        wine = Wine()
        wine["name"]=re.sub("^\d{4} ","",response.xpath("//span[@id='LabelWineTitle']//text() ").extract_first())
        wine["url"] = response.url
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
        for i,score in enumerate(scores):
            if i%2==1:
                average+=score
        wine["score"]= average*2/len(scores)
        #XXX might give error if no rating ?

        wine["winerie"] =response.css('td[id=TableCellBreadCrumb] a::text').extract()[-1]
        
        return wine