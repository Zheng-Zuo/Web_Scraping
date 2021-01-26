import scrapy
from scrapy.http import FormRequest, Request


class ApplicationsSpider(scrapy.Spider):
    name = 'applications'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie']

    def parse(self, response):
        links = response.xpath("//a/@href").getall()
        for link in links:
            if link == '#':
                pass
            else:
                yield Request(url=link,callback=self.parse_application)

    def parse_application(self,response):
        received_app = response.xpath("//*[@class='glyphicon glyphicon-inbox btn-lg']/following-sibling::a/@href").get()
        url = response.urljoin(received_app)
        yield Request(url,callback=self.parse_form)

    def parse_form(self,response):
        yield FormRequest.from_response(response,
                                        formdata={'RdoTimeLimit': '42'},
                                        dont_filter=True,
                                        formxpath='(//form)[2]',
                                        callback=self.parse_pages)

    def parse_pages(self,response):
        links = response.xpath("//td/a/@href").getall()
        for link in links:
            url=response.urljoin(link)
            yield Request(url, callback=self.parse_agents)
        
        next_page = response.xpath('//*[@rel="next"]/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url,callback=self.parse_pages)


    def parse_agents(self,response):
        agent_btn = response.xpath("//input[@value='Agents']/@style").get()
        if "display: inline;  visibility: visible;" in agent_btn:
            agent_name = response.xpath("//tr[th='Name :']/td/text()").get()
            address_1 = response.xpath("//tr[th='Address :']/td/text()").getall()
            address_2 = response.xpath("//tr[th='Address :']/following-sibling::tr/td/text()").getall()[0:3]
            address = address_1+address_2
            phone = response.xpath("//tr[th='Phone :']/td/text()").get()
            fax = response.xpath("//tr[th='Fax :']/td/text()").get()
            email = response.xpath("//tr[th='e-mail :']/td/text()").get()

            yield {'agent_name':agent_name,
                   'address':address,
                   'phone':phone,
                   'fax':fax,
                   'email':email}


        else:
            self.logger.info("Agent button not found")
