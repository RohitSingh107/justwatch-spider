import scrapy
import json

from utils import get_hindi_list_body


COUNT = 165
COUNTRY = "IN"

class HindiListSpider(scrapy.Spider):
    name = "hindi_list"
    allowed_domains = ["apis.justwatch.com"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'justwatch_spider.pipelines.SavingHindiListToPostgresPipeline': 350
        }
    }

    def start_requests(self):

        body = get_hindi_list_body(COUNT, "", COUNTRY)

        yield scrapy.Request(method='POST', body= json.dumps(body), headers={'content-type': 'application/json'}, url='https://apis.justwatch.com/graphql', callback=self.parse)


    def parse(self, response, **kwargs):
        data = response.json()
        for e in data["data"]["genericTitleList"]["edges"]:
            yield { "TITLE" : e["node"]["content"]["title"] + ' ' + str(e["node"]["content"]["originalReleaseYear"])}

        next_page = data["data"]["genericTitleList"]["pageInfo"]["hasNextPage"]
        if next_page:
            cur = data["data"]["genericTitleList"]["pageInfo"]["endCursor"]

            body = get_hindi_list_body(COUNT, cur, COUNTRY)
            yield scrapy.Request(method='POST', body= json.dumps(body), headers={'content-type': 'application/json'}, url='https://apis.justwatch.com/graphql', callback=self.parse)
