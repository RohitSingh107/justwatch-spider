import scrapy
import json

from utils import get_refresh_token_curl, get_access_token_curl, get_headers, get_body
from justwatch_spider.items import TitleItem

class ScrapeSpiderSpider(scrapy.Spider):
    name = "scrape_spider"
    allowed_domains = ["justwatch.com", "identitytoolkit.googleapis.com", "securetoken.googleapis.com"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'justwatch_spider.pipelines.SavingWatchListToPostgresPipeline': 400
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

        for sort_by, list_type in (("RELEASE_YEAR", "WATCHLIST"), ("LAST_ADDED", "SEENLIST")):

            headers = get_headers(access_token)
            json_data = get_body(count, sort_by, list_type)

            body = json.dumps(json_data)

            yield scrapy.Request(method='POST', body = body, headers=headers, url= 'https://apis.justwatch.com/graphql', callback = self.parse, cb_kwargs= {"list_type" : list_type})


    def parse(self, response, **kwargs):
        data = response.json()


        for e in data["data"]["titleListV2"]["edges"]:

            title = TitleItem()

            title["id"] = e["node"]["id"]
            title["title"] = e["node"]["content"]["title"]
            title["runtime"] = e["node"]["content"]["runtime"]
            title["year"] = e["node"]["content"]["originalReleaseYear"]
            title["object_type"] = e["node"]["objectType"]
            title["imdb_score"] = e["node"]["content"]["scoring"]["imdbScore"]
            title["imdb_votes"] = e["node"]["content"]["scoring"]["imdbVotes"]
            title["tmdb_score"] = e["node"]["content"]["scoring"]["tmdbScore"]
            title["tmdb_popularity"] = e["node"]["content"]["scoring"]["tmdbPopularity"]
            title["credits"] = e["node"]["content"]["credits"]
            title["countries"] = e["node"]["content"]["productionCountries"]
            title["list_type"] = kwargs["list_type"]

            yield title
