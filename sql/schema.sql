CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    sector TEXT,
    sponsor_status TEXT,
    careers_url TEXT,
    priority CHAR(1),
    headquarters TEXT,
    notes TEXT
);

CREATE TABLE jobs (
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

CREATE TABLE applications (
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

CREATE TABLE application_events (
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