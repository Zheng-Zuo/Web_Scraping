import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['us-proxy.org']

    script = '''
                function main(splash, args)
                    assert(splash:go(args.url))
                    assert(splash:wait(0.5))
                    treat = require('treat')
                    results = {}
                    for i=1,9,1
                    do
                        splash:select("#proxylisttable_next a").mouse_click()
                        assert(splash:wait(0.5))
                        results[i]= splash:html()
                    end
                    return treat.as_array(results)
                end

    '''

    def start_requests(self):
        url = 'https://us-proxy.org'
        yield SplashRequest(url = url, callback=self.parse, endpoint='render.html',
                            args={'wait':0.5})
        
        yield SplashRequest(url = url, callback=self.parse_pages, endpoint='execute',
                            args={
                                'lua_source': self.script
                            },dont_filter=True)

    def parse(self, response):
        rows = response.xpath("//tbody/tr[@role='row']")
        for row in rows:
            ip =  row.xpath(".//td[1]/text()").get()
            port = row.xpath(".//td[2]/text()").get()

            yield {
                'ip':ip,
                'port':port
            }

    def parse_pages(self,response):
        for page in response.data:
            sel = Selector(text=page)
            rows = sel.xpath("//tbody/tr[@role='row']")
            for row in rows:
                ip =  row.xpath(".//td[1]/text()").get()
                port = row.xpath(".//td[2]/text()").get()

                yield {
                    'ip':ip,
                    'port':port
                }

        
