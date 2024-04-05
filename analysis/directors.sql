SELECT
    movie_directors.name,
    COUNT(*) AS total
FROM
    movie_directors
WHERE
    movie_directors.reference_type = 'SEENLIST'
GROUP BY
    movie_directors.name
ORDER BY
    total DESC;
