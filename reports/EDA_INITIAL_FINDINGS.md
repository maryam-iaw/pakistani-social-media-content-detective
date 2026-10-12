# Exploratory Data Analysis — Initial Findings

## Dataset size
- Records: 2260
- Fields: 13 original fields

## Platform distribution after label normalization

platform_clean
Twitter      745
Instagram    614
Tiktok       398
Facebook     379
Linkedin     124

## Data quality observations
- Platform labels were normalized for this comparison only.
- The original CSV was not modified.
- Country values should be investigated before geographic comparisons.
- Pakistan is not present in the country counts inspected so far.
- Unknown country values must not be assumed to belong to any country.

## Interpretation boundary
These findings describe the starter dataset only. They do not establish
which content types perform best among Pakistani audiences. That requires
a suitable, documented dataset with relevant Pakistani posts and engagement
metrics.

## Generated charts
- `reports/figures/platform_distribution.png`
- `reports/figures/platform_distribution_normalized.png`
- `reports/figures/country_coverage.png`
- `reports/figures/likes_distribution.png`
- `reports/figures/retweets_shares_distribution.png`
- `reports/figures/comments_distribution.png`
