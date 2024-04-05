SELECT
    sorted_by_popularity.rank,
    sorted_by_imdb_score.title AS imdb_score,
    sorted_by_popularity.title AS popularity,
    sorted_by_tmdb_popularity.title AS tmdb_popularity
FROM
    sorted_by_imdb_score
    JOIN sorted_by_popularity ON sorted_by_imdb_score.rank = sorted_by_popularity.rank
    JOIN sorted_by_tmdb_popularity ON sorted_by_tmdb_popularity.rank = sorted_by_popularity.rank;
