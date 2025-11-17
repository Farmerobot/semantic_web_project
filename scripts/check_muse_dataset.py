import csv
from collections import Counter
from pathlib import Path


def main() -> None:
    # Resolve path to project root (this script is assumed to be in <project_root>/scripts).
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent

    # Build relative path to the CSV file
    csv_path = project_root / "data" / "input" / "unprocessed" / "MUSE_dataset.csv"

    if not csv_path.exists():
        print(f"CSV file not found at: {csv_path}")
        return

    rows = []

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)  # skip header
        for row in reader:
            rows.append(tuple(row))  # tuples so they are hashable

    total_rows = len(rows)
    row_counts = Counter(rows)
    duplicate_rows = [row for row, count in row_counts.items() if count > 1]

    print(f"CSV path: {csv_path}")
    print(f"Total data rows (excluding header): {total_rows}")
    print(f"Number of distinct rows: {len(row_counts)}")
    print(f"Number of duplicate rows: {len(duplicate_rows)}")

    if duplicate_rows:
        print("There ARE duplicate rows.")
    else:
        print("No duplicate rows found.")


if __name__ == "__main__":
    main()
