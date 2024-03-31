# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JustwatchSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TitleItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    runtime = scrapy.Field()
    year = scrapy.Field()
    objectType = scrapy.Field()
    imdb_score = scrapy.Field()
    imdb_votes = scrapy.Field()
    tmdb_score = scrapy.Field()
    tmdb_popularity = scrapy.Field()
    credits = scrapy.Field()
    countries = scrapy.Field()
