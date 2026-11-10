# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import pymongo
from itemadapter import ItemAdapter #ItemAdapter wraps different data containers to handle them inn a uniform matter
from scrapy.exceptions import DropItem

class MongoPipeline:
    COLLECTION_NAME = "books" # specifies name of the MongoDB collecction

    #initialises the pipeline
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    #gives access to all core Scrapy components i.e settings
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get("MONGO_URI"),
            mongo_db = crawler.settings.get("MONGO_DATABASE"),
        )

    #opens a connection to mongodb when starts
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    #closes connection
    def close_spider(self, spider):
        self.client.close()

    #inserts each scraped item into the mongodb collection
    def process_item(self, item, spider):
        item_id = self.compute_item_id(item)
        if self.db[self.COLLECTION_NAME].find_one({"_id": item_id}):
            raise DropItem(f"Duplicate item found: {item}")
        else:
            item["_id"] = item_id
            self.db[self.COLLECTION_NAME].insert_one(ItemAdapter(item).asdict())
            return item

    def compute_item_id(self, item):
        url = item["url"]
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

class BooksPipeline:
    def process_item(self, item):
        return item
