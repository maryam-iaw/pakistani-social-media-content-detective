
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "collected"
METADATA_DIR = ROOT / "reports"

REQUIRED_FIELDS = [
    "post_id",
    "timestamp",
    "platform",
    "text",
    "likes",
    "retweets_shares",
    "comments",
]

def validate_records(records):
    """Validate record structure without inventing missing values."""
    if not isinstance(records, list):
        raise ValueError("Input must be a JSON list of records.")

    if not records:
        raise ValueError("No records supplied.")

    df = pd.DataFrame(records)
    missing_fields = [field for field in REQUIRED_FIELDS if field not in df.columns]

    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields}")

    if df["post_id"].isna().any():
        raise ValueError("Some records have missing post_id values.")

    if df["post_id"].duplicated().any():
        raise ValueError("Duplicate post_id values found.")

    return df

def collect_from_json(input_path, source_name):
    """Load records obtained through an approved API or permitted export."""
    input_path = Path(input_path)

    with input_path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    df = validate_records(records)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = OUTPUT_DIR / f"posts_{timestamp}.csv"
    metadata_path = METADATA_DIR / f"collection_{timestamp}.json"

    df.to_csv(output_path, index=False)

    metadata = {
        "source_name": source_name,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_file": str(input_path),
        "output_file": str(output_path.relative_to(ROOT)),
        "record_count": int(len(df)),
        "fields": list(df.columns),
        "required_fields": REQUIRED_FIELDS,
        "notes": (
            "Record the API endpoint, query, date range, license, and applicable "
            "terms before using these data in research."
        ),
    }

    metadata_path.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print(f"Validated records: {len(df)}")
    print(f"CSV saved: {output_path}")
    print(f"Metadata saved: {metadata_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Validate and store records from an approved data source."
    )
    parser.add_argument("--input", required=True, help="Path to a JSON list of records")
    parser.add_argument("--source", required=True, help="Documented source/API name")
    args = parser.parse_args()

    collect_from_json(args.input, args.source)

if __name__ == "__main__":
    main()
