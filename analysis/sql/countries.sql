WITH q1 AS (
    SELECT
        movie_countries.country_id,
        countries.name,
        COUNT(*) AS total
    FROM
        movie_countries
        JOIN countries ON movie_countries.country_id = countries.id
    WHERE
        movie_countries.reference_type = 'SEENLIST'
    GROUP BY
        movie_countries.country_id,
        countries.name
    ORDER BY
        total DESC
),
q2 AS (
    SELECT
        movie_countries.country_id,
        countries.name,
        COUNT(*) AS total
    FROM
        movie_countries
        JOIN countries ON movie_countries.country_id = countries.id
    WHERE
        movie_countries.reference_type = 'WATCHLIST'
    GROUP BY
        movie_countries.country_id,
        countries.name
    ORDER BY
        total DESC
)
SELECT
    COALESCE(q1.name, q2.name) AS country,
    COALESCE(q1.total, 0) AS seenlist,
    COALESCE(q2.total, 0) AS watchlist
FROM
    q1 FULL
    JOIN q2 ON q1.country_id = q2.country_id
ORDER BY
    q1.total DESC NULLS LAST, q2.total DESC NULLS LAST;
