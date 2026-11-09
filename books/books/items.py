# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass


@dataclass
class BooksItem:
    # define the fields for your item here like:
    # name: str | None = None
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
