SELECT *
FROM companies
ORDER BY company_id;

SELECT *
FROM jobs
ORDER BY job_id;

SELECT
    j.job_id,
    c.company_name,
    j.job_title,
    j.location,
    j.salary_min,
    j.salary_max,
    j.employment_type,
    j.sponsorship_status,
    j.job_status
FROM jobs AS j
JOIN companies AS c
    ON j.company_id = c.company_id
ORDER BY j.job_id;