import scrapy
import logging
from scrapy.exceptions import CloseSpider
from scrapy_splash import SplashRequest

class ClasscentralSpider(scrapy.Spider):
    name = 'classcentral'
    allowed_domains = ['www.classcentral.com']
    start_urls = ['https://www.classcentral.com/subjects/']

    def __init__(self,subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            url = response.xpath('//ul/li/h3/a[1][contains(@title,"'+ self.subject + '")]/@href').get()

            if url is None:
                raise CloseSpider(reason="No courses available in this subject...")

            absolute_url = response.urljoin(url)
            yield SplashRequest(url=absolute_url,callback=self.parse_courses,endpoint='render.html',
                                args={'wait':0.5})

        else:
            subjects = response.xpath("//ul/li/h3")
            for subject in subjects:
                url = subject.xpath(".//a[1]/@href").get()
                absolute_url = response.urljoin(url)
                yield SplashRequest(url=absolute_url,callback=self.parse_courses,endpoint='render.html',
                                args={'wait':0.5})

    def parse_courses(self,response):
        courses = response.xpath("//tbody/tr[@itemtype='http://schema.org/Event']")
        for course in courses:
            url = course.xpath(".//td/a/@href").get()
            course_url = response.urljoin(url)
            yield scrapy.Request(url=course_url,callback=self.parse_reviews)

        next_page = response.xpath("//link[@rel='next']/@href").get()
        if next_page:
            absolute_url = response.urljoin(next_page)
            yield SplashRequest(url=absolute_url,callback=self.parse_courses,endpoint='render.html',
                                args={'wait':0.5})


    def parse_reviews(self,response):
        rating = response.xpath("//section[@id='reviews']/header/div/p/strong[1]/text()").get()
        number_of_reviews = response.xpath("//section[@id='reviews']/header/div/p/strong[2]/text()").get()
        name = response.xpath("//h1/text()").get()

        yield {'rating':rating,
               'number_of_reviews':number_of_reviews,
               'name':name}

