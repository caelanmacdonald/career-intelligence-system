CREATE OR REPLACE VIEW application_pipeline AS
SELECT
    a.application_id,
    c.company_name,
    c.sector,
    c.sponsor_status AS company_sponsor_status,
    j.job_title,
    j.location,
    j.salary_min,
    j.salary_max,
    j.sponsorship_status AS role_sponsorship_status,
    a.application_date,
    a.application_status,
    a.current_stage,
    a.cv_version,
    a.cover_letter_used,
    a.follow_up_date,
    a.response_date,
    j.job_url
FROM applications AS a
JOIN jobs AS j
    ON a.job_id = j.job_id
JOIN companies AS c
    ON j.company_id = c.company_id;

CREATE OR REPLACE VIEW follow_up_queue AS
SELECT
    e.event_id,
    e.application_id,
    c.company_name,
    j.job_title,
    e.event_date,
    e.summary AS last_recorded_event,
    e.next_action,
    e.next_action_date,
    CASE
        WHEN e.next_action_date < CURRENT_DATE THEN 'Overdue'
        WHEN e.next_action_date = CURRENT_DATE THEN 'Due today'
        WHEN e.next_action_date <= CURRENT_DATE + 7 THEN 'Due this week'
        ELSE 'Upcoming'
    END AS due_status,
    e.contact_name,
    e.contact_email,
    e.communication_channel
FROM application_events AS e
JOIN applications AS a
    ON e.application_id = a.application_id
JOIN jobs AS j
    ON a.job_id = j.job_id
JOIN companies AS c
    ON j.company_id = c.company_id
WHERE
    e.completed = FALSE
    AND e.next_action IS NOT NULL;