import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest


class BaierlSpider(scrapy.Spider):
    name = 'baierl'
    allowed_domains = ['baierl.com']
    start_urls = ['https://www.baierl.com/new-inventory/']

    def start_requests(self):
        filters_script = """function main(splash)
                                assert(splash:go(splash.args.url))
                                splash:wait(5)

                                local get_element_dim_by_xpath = splash:jsfunc([[
                                    function(xpath) {
                                        var element = document.evaluate(xpath, document, null,
                                            XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                        var element_rect = element.getClientRects()[0];
                                        return {"x": element_rect.left, "y": element_rect.top}
                                    }
                                ]])

                                -- -- Find the YEAR drop down
                                local year_drop_dimensions = get_element_dim_by_xpath(
                                    '//h2[contains(@class, "label ") and contains(text(), "Year ")]')
                                splash:set_viewport_full()
                                splash:mouse_click(year_drop_dimensions.x, year_drop_dimensions.y)
                                splash:wait(1.5)

                                -- -- Clicks the 202X year
                                local year_dimensions = get_element_dim_by_xpath(
                                    '//li[contains(@data-value, "2021")]/span')
                                splash:set_viewport_full()
                                splash:mouse_click(year_dimensions.x, year_dimensions.y)
                                splash:wait(5)

                                -- Find the MAKE drop down
                                local make_drop_dimensions = get_element_dim_by_xpath(
                                    '//h2[contains(@class, "label ") and contains(text(), "Make ")]')
                                splash:set_viewport_full()
                                splash:mouse_click(make_drop_dimensions.x, make_drop_dimensions.y)
                                splash:wait(1.5)

                                -- Clicks the Toyota make
                                local make_dimensions = get_element_dim_by_xpath(
                                    '//li[contains(@data-filters, "make_toyota")]/span')
                                splash:set_viewport_full()
                                splash:mouse_click(make_dimensions.x, make_dimensions.y)
                                splash:wait(5)

                                return splash:html()
                            end"""

        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                endpoint='execute',
                                args={'lua_source': filters_script})

    def parse(self, response):
        cars_urls = response.xpath('//*[@class="title"]/a/@href').extract()
        for car_url in cars_urls:
            absolute_car_url = response.urljoin(car_url)
            yield Request(absolute_car_url,
                          callback=self.parse_car)

        script_at_page_1 = """function main(splash)
                                assert(splash:go(splash.args.url))
                                splash:wait(5)

                                local get_element_dim_by_xpath = splash:jsfunc([[
                                    function(xpath) {
                                        var element = document.evaluate(xpath, document, null,
                                            XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                        var element_rect = element.getClientRects()[0];
                                        return {"x": element_rect.left, "y": element_rect.top}
                                    }
                                ]])

                                -- -- Find the YEAR drop down
                                local year_drop_dimensions = get_element_dim_by_xpath(
                                    '//h2[contains(@class, "label ") and contains(text(), "Year ")]')
                                splash:set_viewport_full()
                                splash:mouse_click(year_drop_dimensions.x, year_drop_dimensions.y)
                                splash:wait(1.5)

                                -- -- Clicks the 202X year
                                local year_dimensions = get_element_dim_by_xpath(
                                    '//li[contains(@data-value, "2021")]/span')
                                splash:set_viewport_full()
                                splash:mouse_click(year_dimensions.x, year_dimensions.y)
                                splash:wait(5)

                                -- Find the MAKE drop down
                                local make_drop_dimensions = get_element_dim_by_xpath(
                                    '//h2[contains(@class, "label ") and contains(text(), "Make ")]')
                                splash:set_viewport_full()
                                splash:mouse_click(make_drop_dimensions.x, make_drop_dimensions.y)
                                splash:wait(1.5)

                                -- Clicks the Toyota make
                                local make_dimensions = get_element_dim_by_xpath(
                                    '//li[contains(@data-filters, "make_toyota")]/span')
                                splash:set_viewport_full()
                                splash:mouse_click(make_dimensions.x, make_dimensions.y)
                                splash:wait(5)

                                next_button = splash:select("*[class='page-next ']")
                                next_button.mouse_click()
                                splash:wait(4)
                                return {
                                    url = splash:url(),
                                    html = splash:html()
                                }
                            end"""

        script_at_page_2 = """function main(splash)
                                assert(splash:go(splash.args.url))
                                splash:wait(5)

                                next_button = splash:select("*[class='page-next ']")
                                next_button.mouse_click()
                                splash:wait(4)
                                return {
                                    url = splash:url(),
                                    html = splash:html()
                                }
                            end"""

        script = None
        if response.url is not self.start_urls[0]:
            script = script_at_page_2
        else:
            script = script_at_page_1

        yield SplashRequest(url=response.url,
                            callback=self.parse,
                            endpoint='execute',
                            args={'lua_source': script})

    def parse_car(self, response):
        name = ''.join(response.xpath('//h1//text()').extract())
        price = response.xpath('//*[@class="finalPrice"]/span/text()').extract_first()
        stock = response.xpath('//li[@class="stock"]/span[@class="value"]/text()').extract_first()

        yield {'name': name,
               'price': price,
               'stock': stock}
