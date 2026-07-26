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