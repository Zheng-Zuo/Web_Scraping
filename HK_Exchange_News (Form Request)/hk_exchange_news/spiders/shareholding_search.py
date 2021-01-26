import scrapy
from scrapy import FormRequest


class SharehodingSearchSpider(scrapy.Spider):
    name = 'shareholding_search'
    allowed_domains = ['www.hkexnews.hk']
    start_urls = ['https://www.hkexnews.hk/sdw/search/searchsdw.aspx']
 

    def parse(self, response):
        view_state = response.xpath("//input[@id='__VIEWSTATE']/@value").get()
        view_state_generator = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get()
        yield FormRequest.from_response(response,    
                                        formdata={
                                        '__EVENTTARGET':'btnSearch',
                                        '__VIEWSTATE':view_state,
                                        '__VIEWSTATEGENERATOR':view_state_generator,
                                        'today':'20210121',
                                        'sortBy':'shareholding',
                                        'sortDirection':'desc',
                                        'txtShareholdingDate':'2021/01/20',
                                        'txtStockCode':'00001'
                                        }, callback= self.parse_item)

    def parse_item(self, response):
        rows = response.xpath("//table[contains(@class,'table')]/tbody/tr")
        for row in rows:
            name = row.xpath(".//td[@class='col-participant-name']/div[2]/text()").get()
            shares = row.xpath(".//td[contains(@class,'col-shareholding')][1]/div[2]/text()").get()

            yield {
                'shareholder_name':name,
                'shares':shares
            }




