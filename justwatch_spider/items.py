# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JustwatchSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



def serialize_null(value):
    if not value or value == 'null':
        return 0
    return value



class TitleItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    runtime = scrapy.Field()
    year = scrapy.Field()
    object_type = scrapy.Field()
    imdb_score = scrapy.Field(serializer = serialize_null)
    imdb_votes = scrapy.Field(serializer = serialize_null)
    tmdb_score = scrapy.Field(serializer = serialize_null)
    tmdb_popularity = scrapy.Field()
    credits = scrapy.Field()
    countries = scrapy.Field()
    list_type = scrapy.Field()
