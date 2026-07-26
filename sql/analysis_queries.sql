-- Employer count by sector
SELECT
    sector,
    COUNT(*) AS employer_count
FROM target_employers
GROUP BY sector
ORDER BY employer_count DESC;


-- Priority split
SELECT
    priority,
    COUNT(*) AS employer_count
FROM target_employers
GROUP BY priority
ORDER BY priority;


-- Priority A employers
SELECT
    company_name,
    sector,
    town_city
FROM target_employers
WHERE priority = 'A'
ORDER BY company_name;