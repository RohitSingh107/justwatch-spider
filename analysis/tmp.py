import psycopg2

q = """
SELECT
  sorted_by_popularity.rank, sorted_by_imdb_score.title as imdb_score, sorted_by_popularity.title as popularity, sorted_by_tmdb_popularity.title as tmdb_popularity
FROM sorted_by_imdb_score
JOIN sorted_by_popularity
  ON sorted_by_imdb_score.rank = sorted_by_popularity.rank
JOIN sorted_by_tmdb_popularity
  ON sorted_by_tmdb_popularity.rank = sorted_by_popularity.rank;

"""

conn = psycopg2.connect(host="localhost", database="postgres", user="rohits")

cur = conn.cursor()

cur.execute(q)

result = cur.fetchall()

all_imdb_score_titles = map(lambda x : x[1], result)
all_popularity_titles = map(lambda x : x[2], result)
all_tmdb_popularity_titles = map(lambda x : x[3], result)

print(list(all_imdb_score_titles))
print("-----------------------------------")
print(list(all_popularity_titles))
print("-----------------------------------")
print(list(all_tmdb_popularity_titles))

