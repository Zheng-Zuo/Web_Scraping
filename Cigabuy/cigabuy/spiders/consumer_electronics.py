import scrapy

class ConsumerelectronicsSpider(scrapy.Spider):
    name = 'consumer_electronics'
    allowed_domains = ['www.cigabuy.com']
    start_urls = ['https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html']

    def parse(self, response):
        
        for item in response.xpath("//div[@class='p_box_wrapper']/div"):
            title = item.xpath(".//div/a[@class='p_box_title']/text()").get()
            link = item.xpath(".//div/a[@class='p_box_title']/@href").get()
         
            discounted_price = item.xpath(".//div/span[@class='productSpecialPrice fl']/text()").get()
            
            if discounted_price:
                normal_price = item.xpath(".//div/span[@class='normalprice fl']/text()").get()
            else:
                discounted_price = item.xpath(".//div[@class='p_box_price cf']/text()").get()
                normal_price = discounted_price

            yield{
                'title': title,
                'discounted_price': discounted_price,
                'normal_price': normal_price,
                'url' : link
            }

        next_page = response.xpath("(//a[@class='nextPage'])[2]/@href").get()

        if next_page:
            yield scrapy.Request(url =next_page, callback= self.parse)
        


