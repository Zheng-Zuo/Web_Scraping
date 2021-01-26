import scrapy


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country']

    def parse(self, response):
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//tbody/tr/td[2]/a/text()").getall()

        yield{
            'title' : title,
            'countries': countries
        }
        

