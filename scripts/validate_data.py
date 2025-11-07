import os
import pandas as pd

DATA_DIR = "data"
REQUIRED_COLUMNS = [
    "doi",
    "year",
    "domain",
    "metric_type",
    "metric_value",
    "validation_type",
    "sample_size",
    "duration_weeks",
    "features",
    "psychometric",
    "notes",
    "validated_by",
]

def validate_csv(path):
    df = pd.read_csv(path)
    problems = []

    # 1) columns
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            problems.append(f"missing column: {col}")

    # 2) empty DOIs
    if "doi" in df.columns:
        empties = df["doi"].isna().sum() + (df["doi"] == "").sum()
        if empties:
            problems.append(f"{empties} rows have empty DOI")

        # 3) duplicate DOIs
        dups = df["doi"].duplicated().sum()
        if dups:
            problems.append(f"{dups} duplicate DOIs")

    return problems

def main():
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".csv"):
            continue
        path = os.path.join(DATA_DIR, fname)
        issues = validate_csv(path)
        if issues:
            print(f"❗ {fname}")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"✅ {fname} looks good")

if __name__ == "__main__":
    main()
