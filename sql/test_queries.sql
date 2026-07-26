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

SELECT
    a.application_id,
    c.company_name,
    j.job_title,
    a.application_date,
    a.application_status,
    a.current_stage,
    a.cv_version,
    a.cover_letter_used,
    a.follow_up_date
FROM applications AS a
JOIN jobs AS j
    ON a.job_id = j.job_id
JOIN companies AS c
    ON j.company_id = c.company_id
ORDER BY a.application_id;

SELECT
    e.event_id,
    c.company_name,
    j.job_title,
    e.event_date,
    e.event_type,
    e.contact_name,
    e.communication_channel,
    e.summary,
    e.next_action,
    e.next_action_date,
    e.completed
FROM application_events AS e
JOIN applications AS a
    ON e.application_id = a.application_id
JOIN jobs AS j
    ON a.job_id = j.job_id
JOIN companies AS c
    ON j.company_id = c.company_id
ORDER BY e.event_date DESC;