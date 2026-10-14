# API Collection Framework

## Purpose
`src/api_collector.py` validates records obtained from an approved API
or permitted data export and saves them as CSV with collection metadata.

## Required fields
- post_id
- timestamp
- platform
- text
- likes
- retweets_shares
- comments

## Usage
Run:

`python src/api_collector.py --input path/to/records.json --source SOURCE_NAME`

The input must be a JSON list of records containing all required fields.
The collector checks required fields, missing post IDs, and duplicate IDs.

## Output
- A timestamped CSV under `data/collected/`
- A timestamped metadata JSON file under `reports/`

## Important limitations
- This is not a live API integration or web scraper.
- The collector does not verify source authenticity, licensing, or API permissions.
- The source, endpoint, query, date range, license, and applicable terms must
  be documented before collecting research data.
- Synthetic test records must not be used as real research observations.
- No conclusions about Pakistani audiences should be drawn without an
  appropriate, documented sample.
