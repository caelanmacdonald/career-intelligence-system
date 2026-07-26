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