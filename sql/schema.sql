CREATE TABLE IF NOT EXISTS companies (
    company_id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    sector TEXT,
    sponsor_status TEXT,
    careers_url TEXT,
    priority CHAR(1),
    headquarters TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    job_title TEXT NOT NULL,
    location TEXT,
    salary_min INTEGER,
    salary_max INTEGER,
    employment_type TEXT,
    sponsorship_status TEXT,
    date_found DATE NOT NULL DEFAULT CURRENT_DATE,
    closing_date DATE,
    job_url TEXT,
    job_status TEXT NOT NULL DEFAULT 'Open',
    notes TEXT,

    CONSTRAINT fk_jobs_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS applications (
    application_id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL,
    application_date DATE NOT NULL DEFAULT CURRENT_DATE,
    application_status TEXT NOT NULL DEFAULT 'Applied',
    current_stage TEXT,
    cv_version TEXT,
    cover_letter_used BOOLEAN NOT NULL DEFAULT FALSE,
    follow_up_date DATE,
    response_date DATE,
    rejection_reason TEXT,
    notes TEXT,

    CONSTRAINT fk_applications_job
        FOREIGN KEY (job_id)
        REFERENCES jobs(job_id)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS application_events (
    event_id SERIAL PRIMARY KEY,
    application_id INTEGER NOT NULL,
    event_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT NOT NULL,
    contact_name TEXT,
    contact_email TEXT,
    communication_channel TEXT,
    summary TEXT NOT NULL,
    next_action TEXT,
    next_action_date DATE,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    notes TEXT,

    CONSTRAINT fk_events_application
        FOREIGN KEY (application_id)
        REFERENCES applications(application_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS target_employers (
    employer_id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL UNIQUE,
    register_name TEXT,
    town_city TEXT,
    county TEXT,
    sector TEXT,
    priority CHAR(1),
    licence_type TEXT,
    visa_route TEXT,
    target_roles TEXT,
    search_frequency TEXT,
    notes TEXT
);

ALTER TABLE target_employers
ADD COLUMN IF NOT EXISTS last_checked TIMESTAMPTZ;

ALTER TABLE target_employers
ADD COLUMN IF NOT EXISTS company_url TEXT;

ALTER TABLE target_employers
ADD COLUMN IF NOT EXISTS careers_url TEXT;

ALTER TABLE target_employers
ADD COLUMN IF NOT EXISTS linkedin_url TEXT;

ALTER TABLE target_employers
ADD COLUMN IF NOT EXISTS links_updated_at TIMESTAMPTZ;

CREATE TABLE IF NOT EXISTS vacancies (

    vacancy_id SERIAL PRIMARY KEY,

    employer_id INTEGER NOT NULL
        REFERENCES target_employers(employer_id),

    title TEXT NOT NULL,

    location TEXT,

    salary TEXT,

    contract_type TEXT,

    closing_date DATE,

    vacancy_url TEXT NOT NULL,

    date_found DATE NOT NULL DEFAULT CURRENT_DATE,

    status TEXT NOT NULL DEFAULT 'Open',

    notes TEXT
);

CREATE TABLE IF NOT EXISTS vacancies (
    vacancy_id SERIAL PRIMARY KEY,

    employer_id INTEGER NOT NULL
        REFERENCES target_employers(employer_id),

    title TEXT NOT NULL,

    location TEXT,
    salary TEXT,
    contract_type TEXT,
    closing_date DATE,

    vacancy_url TEXT NOT NULL,

    date_found DATE NOT NULL DEFAULT CURRENT_DATE,

    status TEXT NOT NULL DEFAULT 'Open',

    notes TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS
    vacancies_vacancy_url_unique
ON vacancies (vacancy_url);