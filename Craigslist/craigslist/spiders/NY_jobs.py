import scrapy
import logging
from scrapy_splash import SplashRequest

class NyJobsSpider(scrapy.Spider):
    name = 'NY_jobs'
    allowed_domains = ['newyork.craigslist.org']

    def start_requests(self):
        yield SplashRequest(url='https://newyork.craigslist.org/search/csr?/',
                            callback=self.parse,
                            endpoint='render.html',
                            args={'wait':0.5})

    def parse(self, response):
        for job in response.xpath("//div[@class='result-info']"):
            title = job.xpath(".//h3/a/text()").get()
            date = job.xpath(".//time/text()").get()
            location = job.xpath(".//span[@class='result-meta']/span[1]/text()").get()
            location = location.replace("(","").replace(")","").strip()
            job_url = job.xpath(".//h3/a/@href").get()
            yield SplashRequest(url=job_url, callback=self.parse_job, endpoint='render.html',
                                args={'wait':0.5},
                                meta={'title': title,
                                      'date': date,
                                      'location': location})

        next_page = response.xpath("(//a[contains(text(),'next ')])[1]/@href").get()
        if next_page:
            absolute_url = response.urljoin(next_page)
            yield SplashRequest(url=absolute_url,
                                callback=self.parse,
                                endpoint='render.html',
                                args={'wait':0.5})
            
    def parse_job(self,response):
        title= response.meta['title']
        date= response.meta['date']
        location= response.meta['location']
        compensation = response.xpath("//p[@class='attrgroup']/span[1]/b/text()").get()
        employment_type = response.xpath("//p[@class='attrgroup']/span[2]/b/text()").get()

        yield {'title':title,
               'date':date,
               'location':location,
               'compensation':compensation,
               'employment_type':employment_type}


