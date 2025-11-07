from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")

REQUIRED = ["doi","year","domain","metric_type","metric_value","validation_type"]

def main():
    for csv_path in DATA_DIR.glob("*.csv"):
        df = pd.read_csv(csv_path)
        problems = []
        # missing columns?
        for col in REQUIRED:
            if col not in df.columns:
                problems.append(f"missing column: {col}")
        # duplicate DOIs?
        if "doi" in df.columns:
            dups = df["doi"].duplicated().sum()
            if dups:
                problems.append(f"{dups} duplicate DOIs")
        if problems:
            print(f"[FAIL] {csv_path.name} → {problems}")
        else:
            print(f"[OK]   {csv_path.name}")

if __name__ == "__main__":
    main()
