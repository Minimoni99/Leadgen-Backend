-- PostgreSQL schema for lead generation platform

CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    category TEXT,
    city TEXT,
    name TEXT,
    address TEXT,
    phone TEXT,
    website TEXT,
    scraped_at TIMESTAMPTZ,
    inserted_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    lead_id INTEGER NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    label TEXT,
    source TEXT,
    verified BOOLEAN DEFAULT FALSE,
    inserted_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(lead_id, email)
);

CREATE TABLE IF NOT EXISTS unsubscribe_list (
    email TEXT PRIMARY KEY,
    unsubscribed_at TIMESTAMPTZ DEFAULT now(),
    reason TEXT,
    source TEXT
);

CREATE TABLE IF NOT EXISTS email_verification (
    email TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    checked_at TIMESTAMPTZ DEFAULT now(),
    details JSONB
);

CREATE TABLE IF NOT EXISTS lead_enrichment (
    lead_id INTEGER PRIMARY KEY REFERENCES leads(id) ON DELETE CASCADE,
    normalized_phone TEXT,
    normalized_website TEXT,
    notes TEXT,
    enrichment_source TEXT,
    enriched_at TIMESTAMPTZ DEFAULT now()
);
