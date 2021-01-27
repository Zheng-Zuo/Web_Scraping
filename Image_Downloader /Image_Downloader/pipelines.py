# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class ImageDownloaderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.images_urls_field, [])
        return [Request(u, meta={'movie_names':item['movie_names']}) for u in urls]

    def file_path(self, request, response=None, info=None, *, item=None):
        movie_names = request.meta['movie_names']
        return (f'full/{movie_names}.jpg').replace("[",'').replace("]",'').replace("'",'').replace('"','')