import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "social_media_sentiment_raw.csv"
REPORT_FILE = ROOT / "reports" / "engagement_metrics.csv"
SUMMARY_FILE = ROOT / "reports" / "ENGAGEMENT_METRICS_FINDINGS.md"

def main():
    df = pd.read_csv(DATA_FILE)

    metrics = ["likes", "retweets_shares", "comments"]
    for col in metrics:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    available = [col for col in metrics if col in df.columns]
    # Negative engagement counts are invalid; exclude them from summaries.
    for col in available:
        df.loc[df[col] < 0, col] = float("nan")
    if not available:
        raise ValueError("No engagement metric columns found.")

    summary = df[available].agg(
        ["count", "mean", "median", "min", "max"]
    ).T
    summary.index.name = "metric"
    summary.to_csv(REPORT_FILE)

    lines = [
        "# Initial Engagement Metrics Analysis",
        "",
        "## Purpose",
        "This report profiles available engagement measures in the starter dataset.",
        "",
        "## Results",
        summary.to_string(),
        "",
        "## Data quality notes",
        f"- Negative likes in source data: {(pd.to_numeric(pd.read_csv(DATA_FILE)['likes'], errors='coerce') < 0).sum()}",
        f"- Missing comments in source data: {pd.to_numeric(pd.read_csv(DATA_FILE)['comments'], errors='coerce').isna().sum()}",
        "- Negative counts are excluded from summary statistics; source data is unchanged.",
        "",
        "## Interpretation limits",
        "- These records have not been established as representative of Pakistani audiences.",
        "- Likes, shares, and comments can vary by platform and audience size.",
        "- This descriptive summary does not establish causation.",
        "- The results must not be presented as findings about Pakistani audiences.",
        "",
        "## Next steps",
        "Repeat this analysis on legally collected, documented data relevant to Pakistan.",
    ]
    SUMMARY_FILE.write_text("\\n".join(lines) + "\\n", encoding="utf-8")
    print(summary)
    print(f"\\nSaved: {REPORT_FILE}")
    print(f"Saved: {SUMMARY_FILE}")

if __name__ == "__main__":
    main()
