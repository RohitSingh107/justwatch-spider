import scrapy
import json


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
        
        body = {
            'operationName': 'GetGenericList',
            'variables': {
                'sortBy': 'NATURAL',
                'sortRandomSeed': 0,
                'platform': 'WEB',
                'listId': 'tl-us-2c7df96d-d4a2-42ca-9b5f-4b098c569d1a',
                'titleListAfterCursor': '',
                'country': COUNTRY,
                'language': 'en',
                'first': COUNT,
                'filter': {
                    'ageCertifications': [],
                    'excludeGenres': [],
                    'excludeProductionCountries': [],
                    'objectTypes': [],
                    'productionCountries': [],
                    'subgenres': [],
                    'genres': [],
                    'packages': [],
                    'excludeIrrelevantTitles': False,
                    'presentationTypes': [],
                    'monetizationTypes': [],
                    'includeTitlesWithoutUrl' : True,
                },
                'watchNowFilter': {
                    'packages': [],
                    'monetizationTypes': [],
                },
            },
            'query': 'query GetGenericList($listId: ID!, $country: Country!, $language: Language!, $first: Int!, $filter: TitleFilter!, $sortBy: GenericTitleListSorting! = POPULAR, $sortRandomSeed: Int! = 0, $watchNowFilter: WatchNowOfferFilter!, $titleListAfterCursor: String, $platform: Platform! = WEB, $profile: PosterProfile, $backdropProfile: BackdropProfile, $format: ImageFormat) {\n  listDetails: node(id: $listId) {\n    ...ListDetails\n    __typename\n  }\n  genericTitleList(\n    id: $listId\n    country: $country\n    after: $titleListAfterCursor\n    first: $first\n    filter: $filter\n    sortBy: $sortBy\n    sortRandomSeed: $sortRandomSeed\n  ) {\n    pageInfo {\n      endCursor\n      hasNextPage\n      hasPreviousPage\n      __typename\n    }\n    totalCount\n    edges {\n      node {\n        ...GenericListTitle\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ListDetails on GenericTitleList {\n  id\n  name\n  type\n  ownedByUser\n  followedlistEntry {\n    createdAt\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment GenericListTitle on MovieOrShow {\n  id\n  objectId\n  objectType\n  content(country: $country, language: $language) {\n    title\n   originalReleaseYear\n    fullPath\n    scoring {\n      imdbScore\n      __typename\n    }\n    posterUrl(profile: $profile, format: $format)\n    ... on ShowContent {\n      backdrops(profile: $backdropProfile, format: $format) {\n        backdropUrl\n        __typename\n      }\n      __typename\n    }\n    isReleased\n    __typename\n  }\n  likelistEntry {\n    createdAt\n    __typename\n  }\n  dislikelistEntry {\n    createdAt\n    __typename\n  }\n  watchlistEntryV2 {\n    createdAt\n    __typename\n  }\n  customlistEntries {\n    createdAt\n    __typename\n  }\n  watchNowOffer(country: $country, platform: $platform, filter: $watchNowFilter) {\n    id\n    standardWebURL\n    package {\n      id\n      packageId\n      clearName\n      __typename\n    }\n    retailPrice(language: $language)\n    retailPriceValue\n    lastChangeRetailPriceValue\n    currency\n    presentationType\n    monetizationType\n    availableTo\n    __typename\n  }\n  ... on Movie {\n    seenlistEntry {\n      createdAt\n      __typename\n    }\n    __typename\n  }\n  ... on Show {\n    seenState(country: $country) {\n      seenEpisodeCount\n      progress\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n',
        }
        yield scrapy.Request(method='POST', body= json.dumps(body), headers={'content-type': 'application/json'}, url='https://apis.justwatch.com/graphql', callback=self.parse)


    def parse(self, response, **kwargs):
        data = response.json()
        for e in data["data"]["genericTitleList"]["edges"]:
            yield { "TITLE" : e["node"]["content"]["title"] + ' ' + str(e["node"]["content"]["originalReleaseYear"])}
