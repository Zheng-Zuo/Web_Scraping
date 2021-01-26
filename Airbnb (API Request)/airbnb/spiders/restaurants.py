import scrapy
import json


class RestaurantsSpider(scrapy.Spider):
    name = 'restaurants'
    allowed_domains = ['airbnb.com']
    start_urls = ['https://www.airbnb.com/s/New-York/things-to-do?refinement_paths%5B%5D=%2Fthings_to_do%2Ffood-restaurants%2Frestaurants&query=New%20York&last_search_session_id=f55fe59e-5499-42a8-aae2-a51526776805&search_type=pagination&click_referer=t%3ASEE_ALL%7Csid%3Af55fe59e-5499-42a8-aae2-a51526776805&tab_id=things_to_do_tab']

    def parse(self, response):
        restaurants = response.xpath("//*[@class='_1nfy29z']/a/@href").getall()
        for restaurent in restaurants:
            restaurent_id = restaurent.split('?')[0].split('/')[-1]
            api_url = f'https://www.airbnb.com/api/v2/places/{restaurent_id}?currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&_format=for_spa_place_view'
            yield scrapy.Request(url=api_url, callback=self.parse_items)

        next_page = response.xpath("//a[@aria-label='Next']/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)

    def parse_items(self,response):
        json_response = json.loads(response.body)
        name = json_response.get('place').get("name")
        address = json_response.get('place').get("address")
        city = json_response.get('place').get("city")
        state = json_response.get('place').get("state")
        zipcode = json_response.get('place').get("zipcode")
        website = json_response.get('place').get("website")
        iphone = json_response.get('place').get("phone")
        yield {'name': name,
               'address': address,
               'city': city,
               'state': state,
               'zipcode': zipcode,
               'website': website,
               'iphone': iphone}




