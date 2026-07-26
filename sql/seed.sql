INSERT INTO companies (
    company_name,
    sector,
    sponsor_status,
    careers_url,
    priority,
    headquarters
)
VALUES
    (
        'Sky',
        'Media',
        'Licensed',
        'https://careers.sky.com',
        'A',
        'London'
    ),
    (
        'Tesco',
        'Retail',
        'Licensed',
        'https://www.tesco-careers.com',
        'A',
        'Welwyn Garden City'
    ),
    (
        'BBC',
        'Media',
        'Licensed',
        'https://careers.bbc.co.uk',
        'A',
        'London'
    );

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