import numpy as np
from pprint import pprint
from collections import defaultdict


# with open("./all_imdb_score.json", 'r') as f:
#     imdb_score_data = json.load(f)
# all_imdb_score_titles = list(map(lambda x : x["node"]["content"]["title"], imdb_score_data["data"]["titleListV2"]["edges"]))
# # print("IMDB SCORE: ", all_imdb_score_titles)
#
#
# with open("./all_popularity.json", 'r') as f:
#     popularity_data = json.load(f)
# all_popularity_titles = list(map(lambda x : x["node"]["content"]["title"], popularity_data["data"]["titleListV2"]["edges"]))
# # print("POPULARITY: ", all_popularity_titles)
#
#
# with open("./all_tmdb_popularity.json", 'r') as f:
#     tmdb_popularity_data = json.load(f)
# all_tmdb_popularity_titles = list(map(lambda x : x["node"]["content"]["title"], tmdb_popularity_data["data"]["titleListV2"]["edges"]))
# # print("TMDB POPULARITY: ", all_tmdb_popularity_titles)


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

cur.execute("SELECT title, imdb_score FROM watchlist ORDER BY imdb_score DESC;")
imdb_score_data = cur.fetchall()

all_imdb_score_titles = list(map(lambda x : x[1], result))
all_popularity_titles = list(map(lambda x : x[2], result))
all_tmdb_popularity_titles = list(map(lambda x : x[3], result))

lists = [all_imdb_score_titles, all_popularity_titles, all_tmdb_popularity_titles]

def write_to_files(file_name, content):
    with open('analysis/output/' + file_name, 'w') as f:
        f.write('\n'.join(content))

def average_rank(lists):
    # Create a dictionary to store the ranks
    rank_dict = {el: [] for lst in lists for el in lst}
    # print(len(rank_dict))

    # Assign ranks
    for lst in lists:
        for rank, el in enumerate(lst, start=1):
            rank_dict[el].append(rank)

    # Calculate average ranks
    avg_ranks = {el: np.mean(ranks) for el, ranks in rank_dict.items()}

    # Create a new list sorted by average rank
    new_list = sorted(avg_ranks, key= avg_ranks.get)
    write_to_files("average_rank.txt", new_list)

    return new_list


def combined_ranks_unweighted(lists):
    # Create a dictionary to hold the total points for each item
    points = defaultdict(int)

    # Calculate the points for each item
    for lst in lists:
        for i, item in enumerate(reversed(lst)):
            points[item] += i + 1

    # Create the combined list
    combined_list = sorted(points, key=points.get, reverse=True)
    write_to_files('combined_ranks_unweighted.txt', combined_list)
    return combined_list


def combined_ranks_weighted(lists):
    # Create a dictionary to hold the total points for each item
    points = defaultdict(int)

    # Calculate the points for each item
    for lst in lists:
        for i, item in enumerate(reversed(lst)):
            points[item] += i + 1



    for t in imdb_score_data:
        points[t[0]] *=  (lambda x : x if x else 1)(t[1])

    # Create the combined list
    combined_list = sorted(points, key=points.get, reverse=True)
    write_to_files('combined_ranks_weighted.txt', combined_list)
    return combined_list


cur.close()
conn.close()


print("-----------------------------------------------------------------------------------------------------------------")
print("AVERAGE RANKS")
result = average_rank(lists)
pprint(result)
print("-----------------------------------------------------------------------------------------------------------------")




print("-----------------------------------------------------------------------------------------------------------------")
print("COMBINED RANKS (UNWEIGHTED)")
result = combined_ranks_unweighted(lists)
pprint(result)
print("-----------------------------------------------------------------------------------------------------------------")



print("-----------------------------------------------------------------------------------------------------------------")
print("COMBINED RANKS (WEIGHTED)")
result = combined_ranks_weighted(lists)
pprint(result)
print("--------------------------------------------")



