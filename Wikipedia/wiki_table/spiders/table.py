import scrapy


class TableSpider(scrapy.Spider):
    name = 'table'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population']

    def parse(self, response):
        rows = response.xpath("//table[@class='wikitable sortable'][1]/tbody/tr")[1:]
        for row in rows:
            rank = row.xpath(".//td[1]/text()").get().strip()
            city = row.xpath(".//td[2]//text()").get()
            state = row.xpath(".//span[@class='flagicon']/following-sibling::a/text()|"
                              ".//span[@class='flagicon']/following-sibling::text()").get().strip()
            yield {
                'rank':rank,
                'city':city,
                'state':state
            }

        
        
