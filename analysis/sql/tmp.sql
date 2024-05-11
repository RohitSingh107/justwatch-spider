SELECT
    w.title
FROM
    watchlist w
    LEFT JOIN movie_countries mc ON w.id = mc.movie
    LEFT JOIN countries c ON mc.country_id = c.id
WHERE
    w.id NOT IN (
        SELECT
            DISTINCT movie
        FROM
            movie_countries
        WHERE
            country_id IN ('IN', 'US')
    )
GROUP BY
    w.title;
