import scrapy
import json

from utils import get_my_list_body, COUNT, COUNTRY


class HotListSpider(scrapy.Spider):
    name = "hot_list"
    allowed_domains = ["apis.justwatch.com"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'justwatch_spider.pipelines.SavingHotListToPostgresPipeline': 350
        }
    }

    def start_requests(self):

        body = get_my_list_body("tl-us-69316e22-d6dd-481a-bf15-7b434f1b80e9", COUNT, "", COUNTRY)

        yield scrapy.Request(method='POST', body= json.dumps(body), headers={'content-type': 'application/json'}, url='https://apis.justwatch.com/graphql', callback=self.parse)


    def parse(self, response, **kwargs):
        data = response.json()
        
        for e in data["data"]["genericTitleList"]["edges"]:
            yield { "TITLE" : e["node"]["content"]["title"] + ' ' + str(e["node"]["content"]["originalReleaseYear"])}

        next_page = data["data"]["genericTitleList"]["pageInfo"]["hasNextPage"]
        if next_page:
            cur = data["data"]["genericTitleList"]["pageInfo"]["endCursor"]

            body = get_my_list_body('tl-us-2c7df96d-d4a2-42ca-9b5f-4b098c569d1a', COUNT, cur, COUNTRY)
            yield scrapy.Request(method='POST', body= json.dumps(body), headers={'content-type': 'application/json'}, url='https://apis.justwatch.com/graphql', callback=self.parse)
