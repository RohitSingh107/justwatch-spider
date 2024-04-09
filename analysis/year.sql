SELECT
    year,
    count(*)
FROM
    seenlist
GROUP BY
    year
ORDER BY
    year DESC;
