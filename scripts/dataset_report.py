import os
import pandas as pd

DATA_DIR = "data"

def report_csv(path):
    df = pd.read_csv(path)
    print(f"\n📘 {os.path.basename(path)}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    # show first 3 rows so you can eyeball it
    print(df.head(3).to_string(index=False))

def main():
    if not os.path.isdir(DATA_DIR):
        print("data/ folder not found")
        return

    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".csv"):
            continue
        report_csv(os.path.join(DATA_DIR, fname))

if __name__ == "__main__":
    main()
