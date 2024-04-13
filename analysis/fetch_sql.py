ALL_SORTINGS = """
SELECT
  sorted_by_popularity.rank, sorted_by_imdb_score.title as imdb_score, sorted_by_popularity.title as popularity, sorted_by_tmdb_popularity.title as tmdb_popularity
FROM sorted_by_imdb_score
JOIN sorted_by_popularity
  ON sorted_by_imdb_score.rank = sorted_by_popularity.rank
JOIN sorted_by_tmdb_popularity
  ON sorted_by_tmdb_popularity.rank = sorted_by_popularity.rank;

"""


async def get_all_sortings(cur):
    await cur.execute(ALL_SORTINGS)
    result = await cur.fetchall()

    all_imdb_score_titles = list(map(lambda x: x[1], result))
    all_popularity_titles = list(map(lambda x: x[2], result))
    all_tmdb_popularity_titles = list(map(lambda x: x[3], result))

    lists = [all_imdb_score_titles,
             all_popularity_titles, all_tmdb_popularity_titles]
    return lists


async def get_all_imdb_score_data(cur):
    await cur.execute("SELECT title, imdb_score FROM watchlist ORDER BY imdb_score DESC;")
    imdb_score_data = await cur.fetchall()
    return imdb_score_data
