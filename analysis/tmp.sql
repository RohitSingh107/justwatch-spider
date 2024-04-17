SELECT
    title
FROM
    movie_genres
JOIN watchlist ON watchlist.id = movie_genres.movie
WHERE
    name = 'Animation';
