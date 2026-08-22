# Sample Scraper CSV

This folder contains an example CSV layout for scraper output.

Columns supported by `src/scraper.py`:

- `business_name`, `name`, `company`, `location_name`
- `address`, `location`
- `phone`, `phone_number`, `tel`, `telephone`
- `website`, `url`
- `email`, `email_address`, `emails`, `contact_email`
- `email_label`, `email_type`
- `category`, `industry`
- `city`, `location_city`
- `scraped_at`, `timestamp`, `date`, `extracted_at`

The importer will normalize these fields and insert them into `leads` and `emails`.
