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