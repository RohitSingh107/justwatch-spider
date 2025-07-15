import scrapy
from utils import get_refresh_token_curl, get_access_token_curl, get_sorting_curl, COUNTRY, COUNT


class SortingSpiderSpider(scrapy.Spider):
    name = "sorting_spider"
    allowed_domains = [
        "justwatch.com", "identitytoolkit.googleapis.com", "securetoken.googleapis.com"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'justwatch_spider.pipelines.SavingSortingsToPostgresPipeline': 325
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

        curls = ((get_sorting_curl(access_token, "", COUNT, sort_by, COUNTRY), sort_by)
                 for sort_by in ["IMDB_SCORE", "POPULAR", "TMDB_POPULARITY"])

        for c, sort_by in curls:
            yield scrapy.Request.from_curl(curl_command=c, callback=self.parse, cb_kwargs={"sort_by": sort_by, "access_token": access_token})

    def parse(self, response, **kwargs):
        sort_by = kwargs["sort_by"]

        data = response.json()
        for e in data["data"]["titleListV2"]["edges"]:
            yield {"ID": e["node"]["id"], "TITLE": e["node"]["content"]["title"], "YEAR":  e["node"]["content"]["originalReleaseYear"], "SORTED BY": sort_by}

        next_page = data["data"]["titleListV2"]["pageInfo"]["hasNextPage"]
        if next_page:
            access_token = kwargs['access_token']
            cur = data["data"]["titleListV2"]["pageInfo"]["endCursor"]
            c = get_sorting_curl(access_token, cur, COUNT, sort_by, COUNTRY)
            yield scrapy.Request.from_curl(curl_command=c, callback=self.parse, cb_kwargs={"sort_by": sort_by, "access_token": access_token})
