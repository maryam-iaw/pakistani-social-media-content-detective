from pathlib import Path
import pandas as pd
import sys

def profile_dataset(input_file, output_file):
    df = pd.read_csv(input_file)
    rows = [{
        "check": "total_rows",
        "column": "all",
        "count": len(df),
        "percentage": 100.0
    }, {
        "check": "duplicate_rows",
        "column": "all",
        "count": int(df.duplicated().sum()),
        "percentage": round(df.duplicated().mean() * 100, 2)
    }]

    for col in df.columns:
        missing = int(df[col].isna().sum())
        rows.append({
            "check": "missing_values",
            "column": col,
            "count": missing,
            "percentage": round(df[col].isna().mean() * 100, 2)
        })

    report = pd.DataFrame(rows)
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(output_file, index=False)
    print(f"Profiled {len(df)} rows across {len(df.columns)} columns.")
    print(f"Saved report to {output_file}")
    return report

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "social_media_sentiment_raw.csv"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "reports/data_quality_summary.csv"
    profile_dataset(input_file, output_file)
