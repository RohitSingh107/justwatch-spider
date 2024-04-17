
WITH query1 AS (
    SELECT
        movie_genres.name AS genre,
        COUNT(*) AS seenlist
    FROM
        movie_genres
    WHERE
        movie_genres.reference_type = 'SEENLIST'
    GROUP BY
        movie_genres.name
),
query2 AS (
    SELECT
        movie_genres.name AS genre,
        COUNT(*) AS watchlist
    FROM
        movie_genres
    WHERE
        movie_genres.reference_type = 'WATCHLIST'
    GROUP BY
        movie_genres.name
)
SELECT
    query2.genre,
    COALESCE(query1.seenlist, 0) as seenlist,
    query2.watchlist
FROM
    query1 FULL
    JOIN query2 ON query1.genre = query2.genre
ORDER BY
    query1.seenlist DESC NULLS LAST;
