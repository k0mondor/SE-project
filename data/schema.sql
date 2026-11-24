CREATE TABLE IF NOT EXISTS chain_segment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    level INTEGER NOT NULL,
    parent_id INTEGER,
    definition TEXT
);

CREATE TABLE IF NOT EXISTS enterprise (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    credit_code TEXT UNIQUE,
    founded_year INTEGER,
    legal_person TEXT,
    reg_capital REAL,
    employee_scale TEXT,
    revenue_scale TEXT,
    industry_code TEXT NOT NULL,
    industry_name TEXT NOT NULL,
    chain_segment TEXT NOT NULL,
    region TEXT NOT NULL,
    production_bases TEXT,
    tech_qualifications TEXT,
    investment_events TEXT,
    source TEXT NOT NULL,
    source_url TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS policy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    region TEXT NOT NULL,
    industry TEXT,
    policy_type TEXT NOT NULL,
    issuer TEXT NOT NULL,
    publish_date TEXT,
    eligibility TEXT,
    content TEXT NOT NULL,
    source_url TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_enterprise_industry ON enterprise(industry_code);
CREATE INDEX IF NOT EXISTS idx_enterprise_segment ON enterprise(chain_segment);
CREATE INDEX IF NOT EXISTS idx_enterprise_region ON enterprise(region);
