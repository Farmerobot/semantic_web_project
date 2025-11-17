import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import statistics

import matplotlib.pyplot as plt
import tiktoken


FALCON_BASE_COLUMNS: List[str] = [
    "new_id",
    "component_id",
    "main_tweet",
    "previous_context",
    "posterior_context",
    "Ad Hominem",
    "Appeal to Fear",
    "Appeal to Ridicule",
    "False Dilemma",
    "Hasty Generalization",
    "Loaded Language",
    "None of the above",
    "created_at",
    "followers",
    "tweet_count",
    "hashtags",
    "cashtags",
    "mentions",
    "retweet_count",
    "reply_count",
    "like_count",
    "quote_count",
    "emojis",
]

FALCON_BASE_DESCRIPTIONS: Dict[str, str] = {
    "new_id": "Unique identifier for each tweet in the FALCON dataset (different from the original Twitter ID).",
    "component_id": "Identifier of the conversation component (thread) the tweet belongs to.",
    "main_tweet": "Text of the tweet that was annotated for fallacies.",
    "previous_context": "Text of context tweets that precede the main tweet (in-neighbors of order 1 or 2).",
    "posterior_context": "Text of context tweets that follow the main tweet (out-neighbors of order 1 or 2).",
    "Ad Hominem": "Binary indicator that the main tweet contains an ad hominem fallacy.",
    "Appeal to Fear": "Binary indicator that the main tweet contains an appeal to fear.",
    "Appeal to Ridicule": "Binary indicator that the main tweet contains an appeal to ridicule.",
    "False Dilemma": "Binary indicator that the main tweet contains a false dilemma.",
    "Hasty Generalization": "Binary indicator that the main tweet contains a hasty generalization.",
    "Loaded Language": "Binary indicator that the main tweet contains loaded language.",
    "None of the above": "Binary indicator that none of the listed fallacy types are present.",
    "created_at": "Timestamp when the main tweet was posted.",
    "followers": "Number of followers of the user who posted the main tweet.",
    "tweet_count": "Total number of tweets posted by the user of the main tweet.",
    "hashtags": "Hashtags present in the main tweet (raw list/text).",
    "cashtags": "Cashtags (e.g. $TSLA) present in the main tweet.",
    "mentions": "User mentions present in the main tweet.",
    "retweet_count": "Number of retweets of the main tweet.",
    "reply_count": "Number of replies to the main tweet.",
    "like_count": "Number of likes of the main tweet.",
    "quote_count": "Number of quote tweets of the main tweet.",
    "emojis": "Emojis present in the main tweet (raw list/text).",
}

FALCON_FALLACY_COLUMNS: List[str] = [
    "Ad Hominem",
    "Appeal to Fear",
    "Appeal to Ridicule",
    "False Dilemma",
    "Hasty Generalization",
    "Loaded Language",
]

FALCON_GROUP_DESCRIPTIONS: Dict[str, str] = {
    "hashtags_": "Binary indicator columns for specific hashtags appearing in the main tweet (e.g. `hashtags_ivermectin`).",
    "mentions_": "Binary indicator columns for specific user mentions appearing in the main tweet.",
    "emojis_": "Binary indicator columns for specific emojis appearing in the main tweet.",
    "VADER_": "Sentiment scores of the main tweet from the VADER tool (negative, neutral, positive, compound).",
    "VAD_": "Valence, arousal, and dominance scores of the main tweet from the NRC-VAD lexicon.",
    "POS_": "Count of tokens with specific part-of-speech tags in the main tweet (e.g. nouns, verbs), from spaCy.",
}

JMBX_DESCRIPTIONS: Dict[str, str] = {
    "ID": "Tweet identifier used in the JMBX dataset.",
    "Number of Likes(favor)": "Number of likes (favorites) the tweet received.",
    "Retweet Count": "Number of retweets of the tweet.",
    "Is retweeted": "Whether the tweet is itself a retweet (True/False).",
    "bias": "Political or ideological bias label (e.g. 'lean left', 'right').",
    "label": "Propaganda technique(s) or rhetorical strategies present in the tweet (list-style string).",
    "slc_label": "Simplified label (e.g. 'propaganda' / 'non-propaganda') summarizing the detailed techniques.",
}

MUSE_DESCRIPTIONS: Dict[str, str] = {
    "created_at": "Timestamp when the note entry was created.",
    "updated_at": "Timestamp when the note entry was last updated.",
    "post_id": "Internal identifier for the post within the dataset.",
    "post_tweet_id": "Original Twitter status ID of the post.",
    "post_text": "Text of the original tweet/post.",
    "response_text": "Text of the explanatory or corrective response (e.g. Community Note / annotation).",
    "response_type": "Source or type of the response (e.g. human-high, human-avg, muse, gpt-4).",
    "annotated": "Whether this datapoint is marked as annotated/valid (e.g. 'Y').",
}


def count_rows_and_header(csv_path: Path) -> Tuple[int, List[str]]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return 0, []
        row_count = sum(1 for _ in reader)
    return row_count, header


def get_project_root() -> Path:
    script_path = Path(__file__).resolve()
    return script_path.parent.parent


def get_falcon_stats(project_root: Path) -> Tuple[int, List[str], List[Path]]:
    base = project_root / "data" / "input" / "unprocessed" / "falcon_dataset"
    split_files = ["df_train.csv", "df_val.csv", "df_test.csv"]
    total_rows = 0
    header: List[str] = []
    csv_paths: List[Path] = []

    for name in split_files:
        path = base / name
        csv_paths.append(path)
        rows, cols = count_rows_and_header(path)
        total_rows += rows
        if not header:
            header = cols

    return total_rows, header, csv_paths


def get_single_csv_stats(csv_path: Path) -> Tuple[int, List[str]]:
    return count_rows_and_header(csv_path)


def render_column_table(columns: List[str], descriptions: Dict[str, str]) -> str:
    lines: List[str] = []
    lines.append("| Column | Description |")
    lines.append("| --- | --- |")
    for col in columns:
        desc = descriptions.get(col, "")
        lines.append(f"| `{col}` | {desc} |")
    return "\n".join(lines)


def summarize_numeric(values: List[float]) -> Dict[str, float]:
    if not values:
        return {"count": 0, "min": 0.0, "max": 0.0, "mean": 0.0, "median": 0.0}
    return {
        "count": float(len(values)),
        "min": float(min(values)),
        "max": float(max(values)),
        "mean": float(statistics.mean(values)),
        "median": float(statistics.median(values)),
    }


def render_numeric_summary_table(title: str, values: List[float]) -> List[str]:
    stats = summarize_numeric(values)
    lines: List[str] = []
    lines.append(f"**{title}**")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("| --- | --- |")
    lines.append(f"| Count | {int(stats['count'])} |")
    lines.append(f"| Min | {stats['min']:.2f} |")
    lines.append(f"| Max | {stats['max']:.2f} |")
    lines.append(f"| Mean | {stats['mean']:.2f} |")
    lines.append(f"| Median | {stats['median']:.2f} |")
    lines.append("")
    return lines


ENCODING = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    if not text:
        return 0
    return len(ENCODING.encode(text))


def render_counter_table(counter: Counter, value_label: str = "Count") -> List[str]:
    lines: List[str] = []
    lines.append("| Value | " + value_label + " |")
    lines.append("| --- | --- |")
    for key, val in counter.most_common():
        lines.append(f"| `{key}` | {val} |")
    lines.append("")
    return lines


def ensure_eda_dirs(project_root: Path) -> Tuple[Path, Path]:
    eda_root = project_root / "data" / "output" / "eda"
    fig_dir = eda_root / "figures"
    eda_root.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    return eda_root, fig_dir


def add_falcon_eda(
    lines: List[str], project_root: Path, falcon_paths: List[Path], fig_dir: Path
) -> None:
    header: List[str] = []
    rows: List[List[str]] = []

    for path in falcon_paths:
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            file_header = next(reader, None)
            if file_header is None:
                continue
            if not header:
                header = file_header
            for row in reader:
                rows.append(row)

    if not header or not rows:
        return

    main_idx = header.index("main_tweet")
    main_texts = [r[main_idx] for r in rows]
    main_len_chars = [len(t) for t in main_texts if t]
    main_len_tokens = [float(count_tokens(t)) for t in main_texts if t]

    fallacy_indices = {
        col: header.index(col)
        for col in FALCON_FALLACY_COLUMNS
        if col in header
    }
    fallacy_counts: Counter = Counter()
    fallacies_per_tweet: List[int] = []

    for r in rows:
        count = 0
        for col, idx in fallacy_indices.items():
            if idx < len(r):
                val = r[idx].strip()
                if val and val not in {"0", "False", "false", "0.0"}:
                    fallacy_counts[col] += 1
                    count += 1
        fallacies_per_tweet.append(count)

    lines.append("")
    lines.append("### Exploratory analysis")
    lines.append("")

    # Length summaries
    lines.extend(render_numeric_summary_table("Length of `main_tweet` in characters", main_len_chars))
    lines.extend(render_numeric_summary_table("Length of `main_tweet` in tokens", main_len_tokens))

    # Fallacy label distribution
    lines.append("**Fallacy label distribution (multi-label counts):**")
    lines.append("")
    lines.extend(render_counter_table(fallacy_counts))

    # Number of fallacies per tweet
    lines.extend(
        render_numeric_summary_table(
            "Number of fallacy labels per tweet", [float(x) for x in fallacies_per_tweet]
        )
    )

    # Histogram: main_tweet length (characters)
    if main_len_chars:
        fig_path = fig_dir / "falcon_main_tweet_len_chars_hist.png"
        plt.figure(figsize=(8, 5))
        plt.hist(main_len_chars, bins=40)
        plt.xlabel("Characters")
        plt.ylabel("Number of tweets")
        plt.title("FALCON main_tweet length (characters)")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        lines.append(
            f"- `main_tweet` length (chars) histogram: `{fig_path.relative_to(project_root).as_posix()}`"
        )

    # Histogram: main_tweet length (tokens)
    if main_len_tokens:
        fig_path = fig_dir / "falcon_main_tweet_len_tokens_hist.png"
        plt.figure(figsize=(8, 5))
        plt.hist(main_len_tokens, bins=40)
        plt.xlabel("Tokens")
        plt.ylabel("Number of tweets")
        plt.title("FALCON main_tweet length (tokens)")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        lines.append(
            f"- `main_tweet` length (tokens) histogram: `{fig_path.relative_to(project_root).as_posix()}`"
        )

    # Bar chart: fallacy label counts
    if fallacy_counts:
        labels = [k for k, _ in fallacy_counts.most_common()]
        values = [fallacy_counts[k] for k in labels]
        fig_path = fig_dir / "falcon_fallacy_label_counts.png"
        plt.figure(figsize=(8, 5))
        plt.bar(labels, values)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Number of tweets")
        plt.title("FALCON fallacy label counts")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        lines.append(
            f"- Fallacy label counts bar chart: `{fig_path.relative_to(project_root).as_posix()}`"
        )

    # Histogram: number of fallacies per tweet
    if fallacies_per_tweet:
        fig_path = fig_dir / "falcon_fallacies_per_tweet_hist.png"
        plt.figure(figsize=(8, 5))
        plt.hist(fallacies_per_tweet, bins=range(0, max(fallacies_per_tweet) + 2))
        plt.xlabel("Number of fallacy labels")
        plt.ylabel("Number of tweets")
        plt.title("FALCON number of fallacies per tweet")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        lines.append(
            f"- Number of fallacies per tweet histogram: `{fig_path.relative_to(project_root).as_posix()}`"
        )


def add_jmbx_eda(lines: List[str], project_root: Path, jmbx_path: Path, fig_dir: Path) -> None:
    if not jmbx_path.exists():
        return

    with jmbx_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return

        try:
            bias_idx = header.index("bias")
            slc_idx = header.index("slc_label")
            likes_idx = header.index("Number of Likes(favor)")
            rt_idx = header.index("Retweet Count")
        except ValueError:
            return

        biases: List[str] = []
        slc_labels: List[str] = []
        likes: List[float] = []
        rts: List[float] = []

        for row in reader:
            if bias_idx < len(row):
                val = row[bias_idx].strip()
                if val:
                    biases.append(val)
            if slc_idx < len(row):
                val = row[slc_idx].strip()
                if val:
                    slc_labels.append(val)
            if likes_idx < len(row):
                val = row[likes_idx].strip()
                if val:
                    try:
                        likes.append(float(val))
                    except ValueError:
                        pass
            if rt_idx < len(row):
                val = row[rt_idx].strip()
                if val:
                    try:
                        rts.append(float(val))
                    except ValueError:
                        pass

    bias_counts = Counter(biases)
    slc_counts = Counter(slc_labels)

    lines.append("")
    lines.append("### Exploratory analysis")
    lines.append("")

    if bias_counts:
        lines.append("**Bias label distribution:**")
        lines.append("")
        lines.extend(render_counter_table(bias_counts))

    if slc_counts:
        lines.append("**Simplified label (`slc_label`) distribution:**")
        lines.append("")
        lines.extend(render_counter_table(slc_counts))

    if likes:
        lines.extend(render_numeric_summary_table("Number of Likes", likes))
    if rts:
        lines.extend(render_numeric_summary_table("Retweet Count", rts))

    if bias_counts:
        labels = [k for k, _ in bias_counts.most_common()]
        values = [bias_counts[k] for k in labels]
        fig_path = fig_dir / "jmbx_bias_counts.png"
        plt.figure(figsize=(8, 5))
        plt.bar(labels, values)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Number of tweets")
        plt.title("JMBX bias label counts")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        lines.append(
            f"- Bias label counts bar chart: `{fig_path.relative_to(project_root).as_posix()}`"
        )

    if slc_counts:
        labels = [k for k, _ in slc_counts.most_common()]
        values = [slc_counts[k] for k in labels]
        fig_path = fig_dir / "jmbx_slc_label_counts.png"
        plt.figure(figsize=(8, 5))
        plt.bar(labels, values)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Number of tweets")
        plt.title("JMBX simplified label (`slc_label`) counts")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        lines.append(
            f"- Simplified label counts bar chart: `{fig_path.relative_to(project_root).as_posix()}`"
        )

    if likes:
        fig_path = fig_dir / "jmbx_likes_hist.png"
        plt.figure(figsize=(8, 5))
        plt.hist(likes, bins=40)
        plt.xlabel("Number of likes")
        plt.ylabel("Number of tweets")
        plt.title("JMBX likes distribution")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        lines.append(
            f"- Likes histogram: `{fig_path.relative_to(project_root).as_posix()}`"
        )

    if rts:
        fig_path = fig_dir / "jmbx_retweets_hist.png"
        plt.figure(figsize=(8, 5))
        plt.hist(rts, bins=40)
        plt.xlabel("Number of retweets")
        plt.ylabel("Number of tweets")
        plt.title("JMBX retweet count distribution")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        lines.append(
            f"- Retweet count histogram: `{fig_path.relative_to(project_root).as_posix()}`"
        )


def add_muse_eda(lines: List[str], project_root: Path, muse_path: Path, fig_dir: Path) -> None:
    if not muse_path.exists():
        return

    with muse_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return

        try:
            post_idx = header.index("post_text")
            resp_idx = header.index("response_text")
            resp_type_idx = header.index("response_type")
            annotated_idx = header.index("annotated")
        except ValueError:
            return

        post_len_chars: List[float] = []
        post_len_tokens: List[float] = []
        resp_len_chars: List[float] = []
        resp_len_tokens: List[float] = []
        resp_types: List[str] = []
        annotated_vals: List[str] = []

        for row in reader:
            if post_idx < len(row):
                t = row[post_idx]
                if t:
                    post_len_chars.append(float(len(t)))
                    post_len_tokens.append(float(count_tokens(t)))
            if resp_idx < len(row):
                t = row[resp_idx]
                if t:
                    resp_len_chars.append(float(len(t)))
                    resp_len_tokens.append(float(count_tokens(t)))
            if resp_type_idx < len(row):
                val = row[resp_type_idx].strip()
                if val:
                    resp_types.append(val)
            if annotated_idx < len(row):
                val = row[annotated_idx].strip()
                if val:
                    annotated_vals.append(val)

    resp_type_counts = Counter(resp_types)
    annotated_counts = Counter(annotated_vals)

    lines.append("")
    lines.append("### Exploratory analysis")
    lines.append("")

    if post_len_chars:
        lines.extend(
            render_numeric_summary_table(
                "Length of `post_text` in characters", post_len_chars
            )
        )
        lines.extend(
            render_numeric_summary_table("Length of `post_text` in tokens", post_len_tokens)
        )

    if resp_len_chars:
        lines.extend(
            render_numeric_summary_table(
                "Length of `response_text` in characters", resp_len_chars
            )
        )
        lines.extend(
            render_numeric_summary_table(
                "Length of `response_text` in tokens", resp_len_tokens
            )
        )

    if resp_type_counts:
        lines.append("**Response type distribution (`response_type`):**")
        lines.append("")
        lines.extend(render_counter_table(resp_type_counts))

    if annotated_counts:
        lines.append("**Annotated flag distribution (`annotated`):**")
        lines.append("")
        lines.extend(render_counter_table(annotated_counts))

    if post_len_chars:
        fig_path = fig_dir / "muse_post_text_len_chars_hist.png"
        plt.figure(figsize=(8, 5))
        plt.hist(post_len_chars, bins=40)
        plt.xlabel("Characters")
        plt.ylabel("Number of posts")
        plt.title("MUSE post_text length (characters)")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        lines.append(
            f"- `post_text` length (chars) histogram: `{fig_path.relative_to(project_root).as_posix()}`"
        )

    if resp_len_chars:
        fig_path = fig_dir / "muse_response_text_len_chars_hist.png"
        plt.figure(figsize=(8, 5))
        plt.hist(resp_len_chars, bins=40)
        plt.xlabel("Characters")
        plt.ylabel("Number of responses")
        plt.title("MUSE response_text length (characters)")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        lines.append(
            f"- `response_text` length (chars) histogram: `{fig_path.relative_to(project_root).as_posix()}`"
        )

    if resp_type_counts:
        labels = [k for k, _ in resp_type_counts.most_common()]
        values = [resp_type_counts[k] for k in labels]
        fig_path = fig_dir / "muse_response_type_counts.png"
        plt.figure(figsize=(8, 5))
        plt.bar(labels, values)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Number of entries")
        plt.title("MUSE response_type counts")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        lines.append(
            f"- response_type counts bar chart: `{fig_path.relative_to(project_root).as_posix()}`"
        )


def generate_markdown_report() -> None:
    project_root = get_project_root()
    eda_root, fig_dir = ensure_eda_dirs(project_root)

    # FALCON stats
    falcon_rows, falcon_header, falcon_paths = get_falcon_stats(project_root)

    # JMBX stats
    jmbx_path = project_root / "data" / "input" / "unprocessed" / "jmbx_dataset.csv"
    jmbx_rows, jmbx_header = get_single_csv_stats(jmbx_path)

    # MUSE stats
    muse_path = project_root / "data" / "input" / "unprocessed" / "MUSE_dataset.csv"
    muse_rows, muse_header = get_single_csv_stats(muse_path)

    lines: List[str] = []
    lines.append("# Dataset statistics and exploratory analysis")
    lines.append("")
    lines.append(f"_Generated on {datetime.utcnow().isoformat(timespec='seconds')}Z_\n")

    # FALCON section
    lines.append("## FALCON")
    lines.append("")
    lines.append("**Files:**")
    for p in falcon_paths:
        rel = p.relative_to(project_root)
        lines.append(f"- `{rel.as_posix()}`")
    lines.append("")
    lines.append(f"**Number of datapoints (rows across all splits):** {falcon_rows}")
    lines.append("")
    lines.append("### Columns")
    lines.append("")
    lines.append("Core columns:")
    lines.append("")
    lines.append(render_column_table(FALCON_BASE_COLUMNS, FALCON_BASE_DESCRIPTIONS))
    lines.append("")
    lines.append("Additional feature groups:")
    lines.append("")
    for prefix, desc in FALCON_GROUP_DESCRIPTIONS.items():
        lines.append(f"- **`{prefix}*`** – {desc}")

    # FALCON EDA
    add_falcon_eda(lines, project_root, falcon_paths, fig_dir)

    # JMBX section
    lines.append("")
    lines.append("## JMBX")
    lines.append("")
    rel_jmbx = jmbx_path.relative_to(project_root)
    lines.append(f"**File:** `{rel_jmbx.as_posix()}`")
    lines.append("")
    lines.append(f"**Number of datapoints (rows):** {jmbx_rows}")
    lines.append("")
    lines.append("### Columns")
    lines.append("")
    lines.append(render_column_table(jmbx_header, JMBX_DESCRIPTIONS))

    # JMBX EDA
    add_jmbx_eda(lines, project_root, jmbx_path, fig_dir)

    # MUSE section
    lines.append("")
    lines.append("## MUSE")
    lines.append("")
    rel_muse = muse_path.relative_to(project_root)
    lines.append(f"**File:** `{rel_muse.as_posix()}`")
    lines.append("")
    lines.append(f"**Number of datapoints (rows):** {muse_rows}")
    lines.append("")
    lines.append("### Columns")
    lines.append("")
    lines.append(render_column_table(muse_header, MUSE_DESCRIPTIONS))

    # MUSE EDA
    add_muse_eda(lines, project_root, muse_path, fig_dir)

    out_path = project_root / "reports/dataset_stats.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote dataset stats and EDA report to: {out_path}")


if __name__ == "__main__":
    generate_markdown_report()
