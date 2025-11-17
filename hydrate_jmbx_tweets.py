import argparse
import json
import os
from typing import List

import pandas as pd
import requests


DEFAULT_CSV_PATH = "data/input/unprocessed/jmbx_dataset.csv"
DEFAULT_OUTPUT_PATH = "data/input/processed/jmbx_hydrated_tweets.json"
API_URL = "https://api.x.com/2/tweets"
MAX_IDS_PER_REQUEST = 100


def load_dataset(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    if "ID" not in df.columns:
        raise ValueError("Expected column 'ID' with tweet IDs in the CSV.")
    if "label" not in df.columns or "slc_label" not in df.columns:
        raise ValueError("Expected columns 'label' and 'slc_label' in the CSV.")
    return df


def print_unique_labels(df: pd.DataFrame) -> None:
    labels = sorted(df["label"].dropna().unique())
    slc_labels = sorted(df["slc_label"].dropna().unique())

    print("Unique values in 'label':")
    for v in labels:
        print(f"  - {v}")

    print("\nUnique values in 'slc_label':")
    for v in slc_labels:
        print(f"  - {v}")


def get_bearer_token() -> str:
    token = os.environ.get("X_BEARER_TOKEN") or os.environ.get("TWITTER_BEARER_TOKEN")
    if not token:
        raise RuntimeError(
            "No X/Twitter bearer token found. Set X_BEARER_TOKEN or TWITTER_BEARER_TOKEN in your environment."
        )
    return token


def chunked(iterable: List[str], size: int) -> List[List[str]]:
    return [iterable[i : i + size] for i in range(0, len(iterable), size)]


def hydrate_tweets(df: pd.DataFrame, max_ids: int | None = None) -> list[dict]:
    ids = df["ID"].astype(str).dropna().unique().tolist()
    if max_ids is not None:
        ids = ids[:max_ids]

    if not ids:
        print("No tweet IDs found to hydrate.")
        return []

    token = get_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    all_tweets: list[dict] = []

    print(f"Hydrating {len(ids)} tweet IDs using X API v2 ...")
    for batch in chunked(ids, MAX_IDS_PER_REQUEST):
        params = {
            "ids": ",".join(batch),
            "tweet.fields": "id,text,created_at,lang,public_metrics,author_id,conversation_id",
        }
        resp = requests.get(API_URL, headers=headers, params=params, timeout=30)
        if resp.status_code != 200:
            print(f"Request failed with status {resp.status_code}: {resp.text}")
            break
        payload = resp.json()
        tweets = payload.get("data", [])
        all_tweets.extend(tweets)
        print(f"  Retrieved {len(tweets)} tweets (total so far: {len(all_tweets)})")

    print(f"Done. Hydrated {len(all_tweets)} tweets.")
    return all_tweets


def save_hydrated_tweets(tweets: list[dict], output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"tweets": tweets}, f, ensure_ascii=False, indent=2)
    print(f"Saved hydrated tweets to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect JMBX dataset and optionally hydrate tweet IDs via X API.")
    parser.add_argument(
        "--csv-path",
        type=str,
        default=DEFAULT_CSV_PATH,
        help="Path to jmbx_dataset.csv (default: %(default)s)",
    )
    parser.add_argument(
        "--hydrate",
        action="store_true",
        help="If set, hydrate tweet IDs to text using the official X API.",
    )
    parser.add_argument(
        "--max-ids",
        type=int,
        default=None,
        help="Optional cap on the number of tweet IDs to hydrate (for testing)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT_PATH,
        help="Output JSON path for hydrated tweets (default: %(default)s)",
    )

    args = parser.parse_args()

    print(f"Loading dataset from: {args.csv_path}")
    df = load_dataset(args.csv_path)
    print(f"Loaded {len(df)} rows.\n")

    print_unique_labels(df)

    if not args.hydrate:
        print("\nHydration not requested (run with --hydrate to fetch tweet text).")
        return

    try:
        tweets = hydrate_tweets(df, max_ids=args.max_ids)
    except RuntimeError as e:
        print(f"Error: {e}")
        return

    if tweets:
        save_hydrated_tweets(tweets, args.output)


if __name__ == "__main__":
    main()
