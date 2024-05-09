SELECT
    w.title,
    w.imdb_score,
    w.tmdb_score,
    string_agg(c.name, ', ') AS countries
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
    w.title,
    w.imdb_score,
    w.tmdb_score
ORDER BY
    w.imdb_score DESC,
    w.tmdb_score DESC;

-- SELECT
--     w.title,
--     w.tmdb_popularity,
--     string_agg(c.name, ', ') AS countries
-- FROM
--     watchlist w
--     LEFT JOIN movie_countries mc ON w.id = mc.movie
--     LEFT JOIN countries c ON mc.country_id = c.id
-- WHERE
--     w.id NOT IN (
--         SELECT
--             DISTINCT movie
--         FROM
--             movie_countries
--         WHERE
--             country_id IN ('IN', 'US')
--     )
-- GROUP BY
--     w.title,
--     w.tmdb_popularity
-- ORDER BY
--     w.tmdb_popularity DESC;
