from scrapy.http import Request
import scrapy
import json


class MenshoesSpider(scrapy.Spider):
    name = 'nikeshoes'
    allowed_domains = ['www.asos.com']
    start_urls = ['https://www.asos.com/men/a-to-z-of-brands/nike/cat/?cid=4766&refine=attribute_1047:8606&nlid=mw|shoes|shop+by+brand']

    def parse(self, response):
        links = response.xpath("//*[@data-auto-id='productTile']")
        for product in links:
            shoe_url = product.xpath(".//a/@href").get()
            product_id = shoe_url.split('?')[0].split('/')[-1]
            api_link = f'https://www.asos.com/api/product/catalogue/v3/stockprice?productIds={product_id}&store=COM&currency=GBP'
            shoe_name = product.xpath(".//p/text()").get()
            yield Request(url=api_link, callback=self.parse_price,meta={'shoe_name':shoe_name})
        
        next_page = response.xpath("//*[@data-auto-id='loadMoreProducts']/@href").get()
        if next_page:
            yield Request(next_page,callback=self.parse)

    def parse_price(self,response):
        page = json.loads(response.body)
        price = page[0]['productPrice']['current']['text']
        yield {
            'Name':response.meta['shoe_name'],
            'price':price
        }
