

import scrapy
from utils import get_refresh_token_curl, get_access_token_curl, get_sorting_curl


class SortingSpiderSpider(scrapy.Spider):
    name = "sorting_spider"
    allowed_domains = ["justwatch.com", "identitytoolkit.googleapis.com", "securetoken.googleapis.com"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'justwatch_spider.pipelines.SavingSortingsToPostgresPipeline': 300
        }
    }

    def start_requests(self):
        c = get_refresh_token_curl()

        yield scrapy.Request.from_curl(curl_command=c, callback=self.access_token)

    def access_token(self, response):
        r = response.json()

        refresh_token = r['refreshToken']

        c = get_access_token_curl(refresh_token)

        yield scrapy.Request.from_curl(curl_command=c, callback=self.fetch_sortings)

    def fetch_sortings(self, response):

        r = response.json()
        access_token = r['access_token']

        count = 165
        curls = ((get_sorting_curl(access_token, count, sort_by), sort_by) for sort_by in ["IMDB_SCORE", "POPULAR", "TMDB_POPULARITY"])

        for c, sort_by in curls:
            yield scrapy.Request.from_curl(curl_command=c, callback = self.parse, cb_kwargs = {"sort_by" : sort_by} )



    def parse(self, response, **kwargs):
        print("Parse function is called")
        data = response.json()
        for e in data["data"]["titleListV2"]["edges"]:
            yield { "TITLE" : e["node"]["content"]["title"], "SORTED BY" : kwargs["sort_by"]}