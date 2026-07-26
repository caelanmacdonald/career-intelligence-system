CREATE OR REPLACE VIEW application_pipeline AS

SELECT
    v.vacancy_id,
    v.employer_id,

    te.company_name,
    te.sector,
    te.priority AS employer_priority,

    v.title AS vacancy_title,
    v.location,
    v.salary,
    v.contract_type,
    v.closing_date,
    v.vacancy_url,
    v.date_found,
    v.status AS vacancy_status,

    a.application_id,
    a.application_date,
    a.application_status,
    a.current_stage,
    a.cv_version,
    a.cover_letter_used,
    a.follow_up_date,
    a.response_date,
    a.rejection_reason,
    a.notes AS application_notes,

    CASE
        WHEN a.application_id IS NULL
            THEN 'Not applied'

        WHEN a.application_status IN (
            'Rejected',
            'Withdrawn',
            'Unsuccessful'
        )
            THEN 'Closed'

        WHEN a.application_status IN (
            'Offer',
            'Accepted'
        )
            THEN 'Successful'

        ELSE 'Active'
    END AS pipeline_category,

    CASE
        WHEN a.follow_up_date IS NULL
            THEN NULL

        WHEN a.follow_up_date < CURRENT_DATE
            THEN 'Overdue'

        WHEN a.follow_up_date = CURRENT_DATE
            THEN 'Due today'

        WHEN a.follow_up_date <= CURRENT_DATE + 7
            THEN 'Due this week'

        ELSE 'Upcoming'
    END AS follow_up_status,

    CASE
        WHEN v.closing_date IS NULL
            THEN NULL

        WHEN v.closing_date < CURRENT_DATE
            THEN 'Closed'

        WHEN v.closing_date = CURRENT_DATE
            THEN 'Closes today'

        WHEN v.closing_date <= CURRENT_DATE + 7
            THEN 'Closes this week'

        ELSE 'Open'
    END AS closing_status,

    CURRENT_DATE - v.date_found
        AS days_since_found,

    CASE
        WHEN a.application_date IS NOT NULL
            THEN a.application_date - v.date_found

        ELSE NULL
    END AS days_found_to_application

FROM vacancies AS v

JOIN target_employers AS te
    ON te.employer_id = v.employer_id

LEFT JOIN applications AS a
    ON a.vacancy_id = v.vacancy_id;

CREATE OR REPLACE VIEW follow_up_queue AS
SELECT
    application_id,
    company_name,
    vacancy_title,
    application_status,
    current_stage,
    follow_up_date,
    follow_up_status,
    vacancy_url
FROM application_pipeline
WHERE follow_up_status IN (
    'Overdue',
    'Due today',
    'Due this week'
)
ORDER BY
    follow_up_date,
    company_name;

CREATE OR REPLACE VIEW employer_summary AS
SELECT
    te.employer_id,
    te.company_name,
    te.sector,
    te.priority,

    COUNT(DISTINCT v.vacancy_id) AS vacancy_count,

    COUNT(DISTINCT a.application_id) AS application_count,

    COUNT(DISTINCT a.application_id)
        FILTER (
            WHERE a.current_stage ILIKE '%interview%'
        ) AS interview_count,

    COUNT(DISTINCT a.application_id)
        FILTER (
            WHERE a.application_status IN (
                'Offer',
                'Accepted'
            )
        ) AS offer_count,

    MAX(v.date_found) AS latest_vacancy_found,

    MAX(a.application_date) AS latest_application_date

FROM target_employers AS te

LEFT JOIN vacancies AS v
    ON v.employer_id = te.employer_id

LEFT JOIN applications AS a
    ON a.vacancy_id = v.vacancy_id

GROUP BY
    te.employer_id,
    te.company_name,
    te.sector,
    te.priority;

CREATE OR REPLACE VIEW follow_up_queue AS
SELECT
    application_id,
    company_name,
    vacancy_title,
    application_status,
    current_stage,
    follow_up_date,
    follow_up_status,
    vacancy_url
FROM application_pipeline
WHERE follow_up_status IN (
    'Overdue',
    'Due today',
    'Due this week'
)
ORDER BY
    follow_up_date,
    company_name;

CREATE OR REPLACE VIEW employer_summary AS
SELECT
    te.employer_id,
    te.company_name,
    te.sector,
    te.priority,

    COUNT(DISTINCT v.vacancy_id) AS vacancy_count,

    COUNT(DISTINCT a.application_id) AS application_count,

    COUNT(DISTINCT a.application_id)
        FILTER (
            WHERE a.current_stage ILIKE '%interview%'
        ) AS interview_count,

    COUNT(DISTINCT a.application_id)
        FILTER (
            WHERE a.application_status IN (
                'Offer',
                'Accepted'
            )
        ) AS offer_count,

    MAX(v.date_found) AS latest_vacancy_found,

    MAX(a.application_date) AS latest_application_date

FROM target_employers AS te

LEFT JOIN vacancies AS v
    ON v.employer_id = te.employer_id

LEFT JOIN applications AS a
    ON a.vacancy_id = v.vacancy_id

GROUP BY
    te.employer_id,
    te.company_name,
    te.sector,
    te.priority;

CREATE OR REPLACE VIEW vacancy_summary AS
SELECT
    COUNT(*) AS total_vacancies,

    COUNT(*) FILTER (
        WHERE vacancy_status = 'Open'
    ) AS open_vacancies,

    COUNT(*) FILTER (
        WHERE vacancy_status = 'Considering'
    ) AS considering_vacancies,

    COUNT(*) FILTER (
        WHERE vacancy_status = 'Applied'
    ) AS applied_vacancies,

    COUNT(*) FILTER (
        WHERE pipeline_category = 'Not applied'
    ) AS not_applied_vacancies,

    COUNT(*) FILTER (
        WHERE closing_status = 'Closes today'
    ) AS closing_today,

    COUNT(*) FILTER (
        WHERE closing_status = 'Closes this week'
    ) AS closing_this_week
FROM application_pipeline;

CREATE OR REPLACE VIEW application_summary AS
SELECT
    COUNT(*) AS total_applications,

    COUNT(*) FILTER (
        WHERE pipeline_category = 'Active'
    ) AS active_applications,

    COUNT(*) FILTER (
        WHERE pipeline_category = 'Closed'
    ) AS closed_applications,

    COUNT(*) FILTER (
        WHERE pipeline_category = 'Successful'
    ) AS successful_applications,

    COUNT(*) FILTER (
        WHERE current_stage ILIKE '%interview%'
    ) AS interview_applications,

    COUNT(*) FILTER (
        WHERE follow_up_status = 'Overdue'
    ) AS overdue_follow_ups,

    COUNT(*) FILTER (
        WHERE follow_up_status = 'Due today'
    ) AS follow_ups_due_today
FROM application_pipeline
WHERE application_id IS NOT NULL;

CREATE OR REPLACE VIEW employer_review_queue AS
SELECT
    employer_id,
    company_name,
    sector,
    priority,
    search_frequency,
    last_checked,
    careers_url,

    CASE
        WHEN last_checked IS NULL
            THEN 'Never checked'

        WHEN search_frequency ILIKE 'Daily'
             AND last_checked < NOW() - INTERVAL '1 day'
            THEN 'Overdue'

        WHEN search_frequency ILIKE 'Weekly'
             AND last_checked < NOW() - INTERVAL '7 days'
            THEN 'Overdue'

        WHEN search_frequency ILIKE 'Monthly'
             AND last_checked < NOW() - INTERVAL '30 days'
            THEN 'Overdue'

        ELSE 'Up to date'
    END AS review_status

FROM target_employers;