import scrapy
from scrapy.loader import ItemLoader
from Image_Downloader.items import ImageDownloaderItem

class MovieCoversSpider(scrapy.Spider):
    name = 'movie_covers'
    allowed_domains = ['https://www.imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?count=100&groups=oscar_best_picture_winners&sort=year%2Cdesc&ref_=nv_ch_osc/']

    def parse(self, response):
        movies = response.xpath("//*[@class='lister-item mode-advanced']")
        for movie in movies:
            url = response.urljoin(movie.xpath(".//h3/a/@href").get())
            yield scrapy.Request(url,callback=self.parse_images, dont_filter=True)

    def parse_images(self, response):
        loader = ItemLoader(item=ImageDownloaderItem(),response=response)
        name = response.xpath("//h1/text()").get().strip()
        image_url = response.xpath("//img/@src").get()
        loader.add_value('image_urls', image_url)
        loader.add_value('movie_names', name)

        yield loader.load_item()
            
            

