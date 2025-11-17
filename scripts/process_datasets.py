import csv
from pathlib import Path
from typing import List


FALCON_SPLITS: List[str] = ["df_train.csv", "df_val.csv", "df_test.csv"]

FALCON_FALLACY_COLUMNS: List[str] = [
    "Ad Hominem",
    "Appeal to Fear",
    "Appeal to Ridicule",
    "False Dilemma",
    "Hasty Generalization",
    "Loaded Language",
    "None of the above",
]


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def process_falcon() -> None:
    project_root = get_project_root()
    falcon_dir = project_root / "data" / "input" / "unprocessed" / "falcon_dataset"
    output_dir = project_root / "data" / "output" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "falcon_processed.csv"

    all_rows = []
    header_written = False

    for split_name in FALCON_SPLITS:
        split_path = falcon_dir / split_name
        if not split_path.exists():
            continue

        with split_path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header is None:
                continue

            try:
                main_idx = header.index("main_tweet")
            except ValueError:
                raise RuntimeError(f"Column 'main_tweet' not found in {split_path}")

            fallacy_indices = {}
            for col in FALCON_FALLACY_COLUMNS:
                if col in header:
                    fallacy_indices[col] = header.index(col)
                else:
                    raise RuntimeError(f"Column '{col}' not found in {split_path}")

            for row in reader:
                if len(row) <= main_idx:
                    continue
                main_text = row[main_idx]

                new_row = [main_text]
                for col in FALCON_FALLACY_COLUMNS:
                    idx = fallacy_indices[col]
                    value = row[idx] if idx < len(row) else ""
                    new_row.append(value)

                all_rows.append(new_row)

    with output_path.open("w", newline="", encoding="utf-8") as out_f:
        writer = csv.writer(out_f)
        header = ["main_tweet"] + FALCON_FALLACY_COLUMNS
        writer.writerow(header)
        writer.writerows(all_rows)

    print(f"Wrote processed FALCON dataset to: {output_path} (rows: {len(all_rows)})")


if __name__ == "__main__":
    process_falcon()
