# Lead Generation Platform

B2B lead sourcing and CRM. Two halves: a **sourcing pipeline** that scrapes and
enriches business leads, and a **CRM** that manages them through a sales pipeline.

## Scope boundary

This project is self-contained in `C:\Users\USER\Projects\leadgen`. It has no
relationship to any other project on this machine. Do not read from, reference,
or reuse code, config, or credentials from anywhere outside this folder.

## Architecture

```
seeds (category x city)
        |
        v
  gosom/google-maps-scraper   <- external tool, run via Docker. NOT forked.
        |                        handles: scraping, proxies, email extraction
        v
    PostgreSQL  <- shared datastore
        |
        v
  CRM app (ours)              <- pipeline, scoring, follow-up, email sequences
```

The scraper is a **dependency, not our source code**. We configure and run it.
We never modify it. If it lacks something, we handle that in our own code
downstream, or contribute upstream.

## Components

| Component | Status | Notes |
|---|---|---|
| Scraper | external | `gosom/google-maps-scraper`, MIT, run via Docker |
| Proxies | not set up | Evomi residential proxies |
| Database | not set up | PostgreSQL, via Docker |
| Seeding | not set up | category x location query generation |
| Enrichment | partial | scraper does email extraction; verification is ours |
| CRM | not started | stack undecided |

## Environment

- Windows 11, PowerShell. `&&` does not work in PS 5.1 — use `;` or `if ($?) {}`.
- Docker Desktop: NOT YET INSTALLED. Required before anything runs.
- Go: not installed. Not needed if we use Docker.

## Conventions

- Never commit `.env`, proxy credentials, or scraped personal data.
- Never edit code directly on the server. Local -> git -> pull on server.
- Every scrape run is reproducible: seed file + config committed, output is not.

## Legal / compliance

Email sequences must have working unsubscribe handling, a real sender address,
and honored opt-outs (CAN-SPAM, GDPR). Build the unsubscribe/suppression tables
into the schema from the start rather than retrofitting.

## Build order

Risk-first. Prove the hard part before paying for infrastructure.

1. Docker installed, scrape 20 leads to CSV locally
2. Postgres locally, scraper writes to DB instead of CSV
3. Seed generation (category x city queue)
4. Evomi proxies, scale to thousands
5. Deploy to Hetzner
6. Email verification pass
7. CRM layer
