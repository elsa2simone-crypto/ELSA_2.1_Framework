#!/usr/bin/env python3
import re
from pathlib import Path
import pandas as pd
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

HEADERS = [
    "doi","year","domain","metric_type","metric_value","validation_type",
    "sample_size","duration_weeks","features","psychometric","notes","validated_by"
]

DOI_RE = re.compile(r"10\.\d{4,9}/\S+")

LAYER_TO_CSV = {
    "somatic": DATA_DIR / "somatic_interoceptive.csv",
    "interoceptive": DATA_DIR / "somatic_interoceptive.csv",
    "emotional": DATA_DIR / "emotional_regulation.csv",
    "emotion": DATA_DIR / "emotional_regulation.csv",
    "cognitive": DATA_DIR / "cognitive_narrative.csv",
    "narrative": DATA_DIR / "cognitive_narrative.csv",
    "social": DATA_DIR / "social_moral.csv",
    "moral": DATA_DIR / "social_moral.csv",
    "cross": DATA_DIR / "cross_layer_coupling.csv",
}

def ensure_csv(path: Path):
    if not path.exists():
        pd.DataFrame(columns=HEADERS).to_csv(path, index=False)

def append_row(csv_path: Path, doi: str, domain_hint: str = ""):
    ensure_csv(csv_path)
    df = pd.read_csv(csv_path)
    if doi in df["doi"].values:
        print(f"• {doi} already in {csv_path.name}")
        return
    new_row = {
        "doi": doi,
        "year": "",
        "domain": domain_hint,
        "metric_type": "",
        "metric_value": "",
        "validation_type": "",
        "sample_size": "",
        "duration_weeks": "",
        "features": "",
        "psychometric": "",
        "notes": "ingested from tagged txt",
        "validated_by": "manual_import_v0.2",
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(csv_path, index=False)
    print(f"✓ {doi} → {csv_path.name}")

def layer_from_tag(line: str):
    line = line.strip().lstrip("#").strip().lower()
    for key in LAYER_TO_CSV:
        if key in line:
            return key
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/ingest_dois.py incoming.txt")
        sys.exit(1)

    txt_path = Path(sys.argv[1])
    if not txt_path.exists():
        print("No such file:", txt_path)
        sys.exit(1)

    # default layer from filename
    default_layer = layer_from_tag(txt_path.name) or "emotional"
    current_layer = default_layer

    for line in txt_path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue

        # tag line?
        tag_layer = layer_from_tag(line)
        if tag_layer:
            current_layer = tag_layer
            continue

        m = DOI_RE.search(line)
        if not m:
            continue
        doi = m.group(0)
        target_csv = LAYER_TO_CSV.get(current_layer, DATA_DIR / "emotional_regulation.csv")
        append_row(target_csv, doi, domain_hint=current_layer)

if __name__ == "__main__":
    main()
