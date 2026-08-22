# Lead Generation Platform

A B2B lead sourcing and CRM platform scaffold.

## Overview

This repository contains the project scaffolding for:

- seed generation (`seeds/generate.py`)
- local PostgreSQL development with Docker
- a minimal lead sourcing pipeline that uses an external scraper

The actual Google Maps scraper is external and run via Docker (`gosom/google-maps-scraper`).

## Local setup

1. Install Docker Desktop on Windows.
2. Copy `.env.example` to `.env`.
3. Start PostgreSQL locally:

```powershell
docker compose up -d
```

4. Generate seed queries:

```powershell
py -m leadgen.cli seed
```

5. Use the generated `seeds/queries.txt` as input to your scraper.

6. Import scraper output into PostgreSQL:

```powershell
py -m leadgen.cli import samples/scraper-sample.csv
```

7. Run enrichment on pending leads:

```powershell
py -m leadgen.cli enrich --batch-size 100
```

### Scraper and proxy integration

The scraper is external and runs in Docker using seed queries from `seeds/queries.txt`.
Use `scripts/run-scraper.ps1` to start the scraper with optional proxy support.

```powershell
cd c:\Users\USER\Projects\leadgen\scripts
.\run-scraper.ps1
```

By default it mounts `seeds/queries.txt` and writes output to `output/scraper-results.csv`.

You can configure proxies in `.env` using one of these options:

	- `PROXY_HOST` / `PROXY_PORT` / `PROXY_PROTOCOL` / `PROXY_USER` / `PROXY_PASS`
	- `PROXIES=http://user:pass@proxy1:8000,socks5://user:pass@proxy2:1080`
	- `PROXY_FILE=proxies.txt`

`proxies.txt` should contain one proxy URL per line.

### Docker helper

You can also run the Python tooling from Docker without installing Python locally:

```powershell
docker compose build tool
docker compose run --rm tool seed
```

You can use the same pattern for database initialization and importing:

```powershell
docker compose run --rm tool init
docker compose run --rm tool import samples/scraper-sample.csv
```

### Bootstrap helper

Use the provided PowerShell helper to install dependencies and initialize the database.

```powershell
cd c:\Users\USER\Projects\leadgen\scripts
.\bootstrap.ps1
```

If Docker is available, it will build the tool image, start the database, and initialize the schema. If only Python is available, it will run the package CLI locally.

### Verify the scaffold

Run the built-in tests to validate the generator and scraper normalization.

```powershell
cd c:\Users\USER\Projects\leadgen
py -m pytest -q
```

If using Docker:

```powershell
docker compose run --rm tool pytest -q
```

Or use the helper scripts:

```powershell
cd c:\Users\USER\Projects\leadgen\scripts
.\verify.ps1
.\test.ps1
```

`verify.ps1` runs package tests using Python or Docker. `test.ps1` is an explicit one-line test runner.

## PostgreSQL service

The local database service is defined in `docker-compose.yml`:

- `db` runs PostgreSQL 15
- data is stored in a Docker volume named `leadgen_pgdata`
- credentials are configured via `.env`

## Seed generation

`seeds/generate.py` creates a `seeds/queries.txt` file using category and city combinations.

## Notes

- Do not commit `.env` or scraped output.
- The repository intentionally keeps scraped data out of source control.
- This scaffold is a starting point; the next step is wiring the scraper output into PostgreSQL.

## Evomi and paid proxies

If you choose Evomi (or any paid proxy provider) you must purchase a plan and obtain proxy credentials from the provider. Do not commit credentials to source control.

Use the interactive helper to store credentials locally in `.env`:

```powershell
cd c:\Users\USER\Projects\leadgen\scripts
.\set-evomi.ps1
```

Alternatively, create a `proxies.txt` file with one proxy URL per line and set `PROXY_FILE=proxies.txt` in `.env`.

When you have valid proxy credentials and want me to guide you through the next steps (for example enabling proxy rotation, tuning concurrency, or running a validation scrape), tell me and I will prompt you for the non-sensitive configuration choices. Never paste secrets into this chat; keep them in `.env` locally.
