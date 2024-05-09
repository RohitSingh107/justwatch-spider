SELECT
    movie_cast.name,
    COUNT(*) AS total
FROM
    movie_cast
WHERE
    movie_cast.reference_type = 'SEENLIST'
GROUP BY
    movie_cast.name
ORDER BY
    total DESC;

SELECT
    title,
    year,
    name,
    reference_type
FROM
    movie_cast
    JOIN seenlist ON seenlist.id = movie_cast.movie
WHERE
    name = 'Michael Caine';

SELECT
    title,
    year,
    name,
    reference_type
FROM
    movie_cast
    JOIN seenlist ON seenlist.id = movie_cast.movie
WHERE
    name = 'Hugh Jackman';

SELECT
    title,
    year,
    name,
    reference_type
FROM
    movie_cast
    JOIN seenlist ON seenlist.id = movie_cast.movie
WHERE
    name = 'Patrick Stewart';

SELECT
    title,
    year,
    name,
    reference_type
FROM
    movie_cast
    JOIN seenlist ON seenlist.id = movie_cast.movie
WHERE
    name = 'Cillian Murphy';

SELECT
    title,
    year,
    name,
    reference_type
FROM
    movie_cast
    JOIN seenlist ON seenlist.id = movie_cast.movie
WHERE
    name = 'Christian Bale';

SELECT
    title,
    year,
    name,
    reference_type
FROM
    movie_cast
    JOIN seenlist ON seenlist.id = movie_cast.movie
WHERE
    name = 'Morgan Freeman ';

SELECT
    title,
    year,
    name,
    reference_type
FROM
    movie_cast
    JOIN seenlist ON seenlist.id = movie_cast.movie
WHERE
    name = 'Gary Oldman';

SELECT
    title,
    year,
    name,
    reference_type
FROM
    movie_cast
    JOIN seenlist ON seenlist.id = movie_cast.movie
WHERE
    name = 'David Dastmalchian';
