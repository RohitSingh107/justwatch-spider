from secret import API_KEY, EMAIL, PASSWORD

# From curl is not a good idea because of {} and syntax errors


def get_refresh_token_curl():
    return f"""
curl 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}' \
  -X POST \
  -H 'Content-Type: application/json' \
  --data-raw '{{"returnSecureToken":true,"email":"{EMAIL}","password":"{PASSWORD}","clientType":"CLIENT_TYPE_WEB"}}'
"""


def get_access_token_curl(refreshToken: str):
    return f"""
curl 'https://securetoken.googleapis.com/v1/token?key={API_KEY}' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-raw 'grant_type=refresh_token&refresh_token={refreshToken}'

"""


def get_sorting_curl(token: str, cursor: str, count: int, sort_by: str, country : str):
    return f"""
curl 'https://apis.justwatch.com/graphql' \
  -X POST \
  -H 'content-type: application/json' \
  -H 'Authorization: Bearer {token}' \
  --data-raw '{{
  "operationName": "GetTitleListV2",
  "variables": {{
    "titleListSortBy": "{sort_by}",
    "first": {count},
    "sortRandomSeed": 0,
    "platform": "WEB",
    "includeOffers": false,
    "titleListFilter": {{
      "ageCertifications": [],
      "excludeGenres": [],
      "excludeProductionCountries": [],
      "objectTypes": [],
      "productionCountries": [],
      "genres": [],
      "packages": [],
      "excludeIrrelevantTitles": false,
      "presentationTypes": [],
      "monetizationTypes": [],
      "subgenres": [],
      "includeTitlesWithoutUrl" : true
    }},
    "watchNowFilter": {{ "packages": [], "monetizationTypes": [] }},
    "language": "en",
    "country": "{country}",
    "titleListType": "WATCHLIST",
    "titleListAfterCursor": "{cursor}"
  }},
  "query": "\\nquery GetTitleListV2(\\n  $country: Country!\\n  $titleListFilter: TitleFilter\\n  $titleListSortBy: TitleListSortingV2! = LAST_ADDED\\n  $titleListType: TitleListTypeV2!\\n  $titleListAfterCursor: String\\n  $watchNowFilter: WatchNowOfferFilter!\\n  $first: Int! = 10\\n  $language: Language!\\n  $sortRandomSeed: Int! = 0\\n  $profile: PosterProfile\\n  $backdropProfile: BackdropProfile\\n  $format: ImageFormat\\n  $platform: Platform! = WEB\\n  $includeOffers: Boolean = false\\n) {{\\n  titleListV2(\\n    after: $titleListAfterCursor\\n    country: $country\\n    filter: $titleListFilter\\n    sortBy: $titleListSortBy\\n    first: $first\\n    titleListType: $titleListType\\n    sortRandomSeed: $sortRandomSeed\\n  ) {{\\n    totalCount\\n    pageInfo {{\\n      startCursor\\n      endCursor\\n      hasPreviousPage\\n      hasNextPage\\n      __typename\\n    }}\\n    edges {{\\n      ...WatchlistTitleGraphql\\n      __typename\\n    }}\\n    __typename\\n  }}\\n}}\\nfragment WatchlistTitleGraphql on TitleListEdgeV2 {{\\n  cursor\\n  node {{\\n    id\\n    objectId\\n    objectType\\n    offerCount(country: $country, platform: $platform)\\n    offers(country: $country, platform: $platform)\\n      @include(if: $includeOffers) {{\\n      id\\n      presentationType\\n      monetizationType\\n      retailPrice(language: $language)\\n      type\\n      package {{\\n        id\\n        packageId\\n        clearName\\n        __typename\\n      }}\\n      standardWebURL\\n      elementCount\\n      deeplinkRoku: deeplinkURL(platform: ROKU_OS)\\n      __typename\\n    }}\\n    content(country: $country, language: $language) {{\\n      title\\n      fullPath\\n      originalReleaseYear\\n      shortDescription\\n      scoring {{\\n        imdbScore\\n        imdbVotes\\n        tmdbScore\\n        tmdbPopularity\\n        __typename\\n      }}\\n      posterUrl(profile: $profile, format: $format)\\n      backdrops(profile: $backdropProfile, format: $format) {{\\n        backdropUrl\\n        __typename\\n      }}\\n      upcomingReleases(releaseTypes: [DIGITAL]) {{\\n        releaseDate\\n        __typename\\n      }}\\n      isReleased\\n      __typename\\n    }}\\n    likelistEntry {{\\n      createdAt\\n      __typename\\n    }}\\n    dislikelistEntry {{\\n      createdAt\\n      __typename\\n    }}\\n    watchlistEntryV2 {{\\n      createdAt\\n      __typename\\n    }}\\n    customlistEntries {{\\n      createdAt\\n      __typename\\n    }}\\n    watchNowOffer(\\n      country: $country\\n      platform: $platform\\n      filter: $watchNowFilter\\n    ) {{\\n      id\\n      standardWebURL\\n      package {{\\n        id\\n        packageId\\n        clearName\\n        __typename\\n      }}\\n      retailPrice(language: $language)\\n      retailPriceValue\\n      currency\\n      lastChangeRetailPriceValue\\n      presentationType\\n      monetizationType\\n      availableTo\\n      __typename\\n    }}\\n    ... on Movie {{\\n      seenlistEntry {{\\n        createdAt\\n        __typename\\n      }}\\n      __typename\\n    }}\\n    ... on Show {{\\n      tvShowTrackingEntry {{\\n        createdAt\\n        __typename\\n      }}\\n      seenState(country: $country) {{\\n        seenEpisodeCount\\n        releasedEpisodeCount\\n        progress\\n        caughtUp\\n        lastSeenEpisodeNumber\\n        lastSeenSeasonNumber\\n        __typename\\n      }}\\n      __typename\\n    }}\\n    __typename\\n  }}\\n  __typename\\n}}\\n\\n\\n"
}}'
"""


def get_headers(token):
    return {
        "content-type": "application/json",
        "Authorization": f"Bearer {token}",
    }


def get_body(count : int, cursor: str, sort_by : str, list_type : str, country : str):
    return {
        'operationName': 'GetTitleListV2',
        'variables': {
            'titleListSortBy': sort_by,
            'first': count,
            'sortRandomSeed': 0,
            'platform': 'WEB',
            'includeOffers': False,
            'titleListFilter': {
                'ageCertifications': [],
                'excludeGenres': [],
                'excludeProductionCountries': [],
                'objectTypes': [],
                'productionCountries': [],
                'genres': [],
                'packages': [],
                'excludeIrrelevantTitles': False,
                'presentationTypes': [],
                'monetizationTypes': [],
                'subgenres': [],
                'includeTitlesWithoutUrl' : True,
            },
            'watchNowFilter': {
                'packages': [],
                'monetizationTypes': [],
            },
            'language': 'en',
            'country': country,
            'titleListType': list_type,
            'titleListAfterCursor': cursor,
        },
        'query': '\nquery GetTitleListV2(\n  $country: Country!\n  $titleListFilter: TitleFilter\n  $titleListSortBy: TitleListSortingV2! = LAST_ADDED\n  $titleListType: TitleListTypeV2!\n  $titleListAfterCursor: String\n    $first: Int! = 10\n  $language: Language!\n  $sortRandomSeed: Int! = 0\n      $platform: Platform! = WEB\n  $includeOffers: Boolean = false\n) {\n  titleListV2(\n    after: $titleListAfterCursor\n    country: $country\n    filter: $titleListFilter\n    sortBy: $titleListSortBy\n    first: $first\n    titleListType: $titleListType\n    sortRandomSeed: $sortRandomSeed\n  ) {\n    totalCount\n    pageInfo {\n      startCursor\n      endCursor\n      hasPreviousPage\n      hasNextPage\n          }\n    edges {\n      ...WatchlistTitleGraphql\n          }\n      }\n}\nfragment WatchlistTitleGraphql on TitleListEdgeV2 {\n  cursor\n  node {\n    id\n    objectId\n    objectType\n       offers(country: $country, platform: $platform)\n      @include(if: $includeOffers) {\n      id\n      presentationType\n      monetizationType\n      retailPrice(language: $language)\n      type\n      package {\n        id\n        packageId\n        clearName\n              }\n      standardWebURL\n      elementCount\n      deeplinkRoku: deeplinkURL(platform: ROKU_OS)\n          }\n   popularityRank(country: $country) {\n          rank\n  }\n    content(country: $country, language: $language) {\n      title\n     runtime\n    genres {\n            shortName\n         }\n     credits { role name }\n     productionCountries\n       originalReleaseYear\n      shortDescription\n      scoring {\n        imdbScore\n        imdbVotes\n        tmdbScore\n        tmdbPopularity\n      jwRating\n        }\n                      }\n      }\n  }\n\n\n',
    }




def expand_genre(genre : str):
    match genre:
        case "drm":
            return "Drama"
        case "trl":
            return "Mystry & Thriller"
        case "cmy":
            return "Comedy"
        case "rma":
            return "Romance"
        case "act":
            return "Action"
        case "crm":
            return "Crime"
        case "scf":
            return "Science-Fiction"
        case "hrr":
            return "Horror"
        case "eur":
            return "Made in Europe"
        case "fnt":
            return "Fantasy"
        case "hst":
            return "History"
        case "doc":
            return "Documentary"
        case "war":
            return "War & Military"
        case "msc":
            return "Music"
        case "wsn":
            return "Western"
        case "fml":
            return "Family"
        case "rly":
            return "Reality TV"
        case "spt":
            return "Sport"
        case "ani":
            return "Animation"
        case _:
            return genre
