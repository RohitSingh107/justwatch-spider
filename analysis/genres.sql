SELECT
    movie_genres.name as SEENLIST,
    COUNT(*) AS total
FROM
    movie_genres
WHERE
    movie_genres.reference_type = 'SEENLIST'
GROUP BY
    movie_genres.name
ORDER BY
    total DESC;

SELECT
    movie_genres.name as WATCHLIST,
    COUNT(*) AS total
FROM
    movie_genres
WHERE
    movie_genres.reference_type = 'WATCHLIST'
GROUP BY
    movie_genres.name
ORDER BY
    total DESC;
