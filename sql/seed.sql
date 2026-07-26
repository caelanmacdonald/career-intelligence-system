INSERT INTO jobs (
    company_id,
    job_title,
    location,
    salary_min,
    salary_max,
    employment_type,
    sponsorship_status,
    job_url
)
VALUES (
    1,
    'Junior BI Analyst',
    'London',
    35000,
    42000,
    'Permanent',
    'Unknown',
    'https://example.com/job'
);

INSERT INTO applications (
    job_id,
    application_status,
    current_stage,
    cv_version,
    cover_letter_used,
    follow_up_date,
    notes
)
VALUES (
    1,
    'Applied',
    'Application submitted',
    'BI CV v1',
    TRUE,
    CURRENT_DATE + 14,
    'Test application record'
);

INSERT INTO application_events (
    application_id,
    event_type,
    contact_name,
    communication_channel,
    summary,
    next_action,
    next_action_date
)
VALUES (
    1,
    'Application submitted',
    NULL,
    'Employer website',
    'Submitted application for the Junior BI Analyst role.',
    'Follow up if no response',
    CURRENT_DATE + 14
);