SELECT
    year,
    count(*)
FROM
    seenlist
GROUP BY
    year
ORDER BY
    year DESC;

-- SELECT
--     year,
--     count(*)
-- FROM
--     watchlist
-- GROUP BY
--     year
-- ORDER BY
--     year DESC;
