import scrapy


class PopulationbycountriesSpider(scrapy.Spider):
    name = 'populationbycountries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country']

    def parse(self, response):
        
        country_tags = response.xpath("//tbody/tr/td[2]/a")

        for country in country_tags:
            country_name = country.xpath(".//text()").get()
            country_link = country.xpath(".//@href").get()

            absolute_url = response.urljoin(country_link)

            yield scrapy.Request(url= absolute_url, callback= self.parse_country, meta={'country': country_name})

    def parse_country(self, response):

        for pop in response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr"):
            year = pop.xpath(".//td[1]/text()").get()
            population = pop.xpath(".//td[2]/strong/text()").get()
            country_name = response.request.meta['country']

            yield{
                'country_name':country_name,
                'year': year,
                'population': population
            }

        

