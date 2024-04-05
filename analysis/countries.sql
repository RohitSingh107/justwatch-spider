

SELECT
    movie_countries.country_id,
    COUNT(*) AS total,
    countries.name
FROM
    movie_countries
JOIN
    countries ON movie_countries.country_id = countries.id
WHERE
    movie_countries.reference_type = 'SEENLIST'
GROUP BY
    movie_countries.country_id, countries.name
ORDER BY
    total DESC;
