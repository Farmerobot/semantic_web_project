# Dataset statistics and exploratory analysis

_Generated on 2025-11-17T12:57:06Z_

## FALCON

**Files:**
- `data/input/unprocessed/falcon_dataset/df_train.csv`
- `data/input/unprocessed/falcon_dataset/df_val.csv`
- `data/input/unprocessed/falcon_dataset/df_test.csv`

**Number of datapoints (rows across all splits):** 2916

### Columns

Core columns:

| Column | Description |
| --- | --- |
| `new_id` | Unique identifier for each tweet in the FALCON dataset (different from the original Twitter ID). |
| `component_id` | Identifier of the conversation component (thread) the tweet belongs to. |
| `main_tweet` | Text of the tweet that was annotated for fallacies. |
| `previous_context` | Text of context tweets that precede the main tweet (in-neighbors of order 1 or 2). |
| `posterior_context` | Text of context tweets that follow the main tweet (out-neighbors of order 1 or 2). |
| `Ad Hominem` | Binary indicator that the main tweet contains an ad hominem fallacy. |
| `Appeal to Fear` | Binary indicator that the main tweet contains an appeal to fear. |
| `Appeal to Ridicule` | Binary indicator that the main tweet contains an appeal to ridicule. |
| `False Dilemma` | Binary indicator that the main tweet contains a false dilemma. |
| `Hasty Generalization` | Binary indicator that the main tweet contains a hasty generalization. |
| `Loaded Language` | Binary indicator that the main tweet contains loaded language. |
| `None of the above` | Binary indicator that none of the listed fallacy types are present. |
| `created_at` | Timestamp when the main tweet was posted. |
| `followers` | Number of followers of the user who posted the main tweet. |
| `tweet_count` | Total number of tweets posted by the user of the main tweet. |
| `hashtags` | Hashtags present in the main tweet (raw list/text). |
| `cashtags` | Cashtags (e.g. $TSLA) present in the main tweet. |
| `mentions` | User mentions present in the main tweet. |
| `retweet_count` | Number of retweets of the main tweet. |
| `reply_count` | Number of replies to the main tweet. |
| `like_count` | Number of likes of the main tweet. |
| `quote_count` | Number of quote tweets of the main tweet. |
| `emojis` | Emojis present in the main tweet (raw list/text). |

Additional feature groups:

- **`hashtags_*`** – Binary indicator columns for specific hashtags appearing in the main tweet (e.g. `hashtags_ivermectin`).
- **`mentions_*`** – Binary indicator columns for specific user mentions appearing in the main tweet.
- **`emojis_*`** – Binary indicator columns for specific emojis appearing in the main tweet.
- **`VADER_*`** – Sentiment scores of the main tweet from the VADER tool (negative, neutral, positive, compound).
- **`VAD_*`** – Valence, arousal, and dominance scores of the main tweet from the NRC-VAD lexicon.
- **`POS_*`** – Count of tokens with specific part-of-speech tags in the main tweet (e.g. nouns, verbs), from spaCy.

### Exploratory analysis

**Length of `main_tweet` in characters**

| Metric | Value |
| --- | --- |
| Count | 2916 |
| Min | 37.00 |
| Max | 321.00 |
| Mean | 193.61 |
| Median | 201.00 |

**Length of `main_tweet` in tokens**

| Metric | Value |
| --- | --- |
| Count | 2916 |
| Min | 12.00 |
| Max | 122.00 |
| Mean | 48.96 |
| Median | 50.00 |

**Fallacy label distribution (multi-label counts):**

| Value | Count |
| --- | --- |
| `Loaded Language` | 457 |
| `Ad Hominem` | 259 |
| `Appeal to Ridicule` | 238 |
| `False Dilemma` | 168 |
| `Appeal to Fear` | 157 |
| `Hasty Generalization` | 91 |

**Number of fallacy labels per tweet**

| Metric | Value |
| --- | --- |
| Count | 2916 |
| Min | 0.00 |
| Max | 4.00 |
| Mean | 0.47 |
| Median | 0.00 |

- `main_tweet` length (chars) histogram: `data/output/eda/figures/falcon_main_tweet_len_chars_hist.png`
- `main_tweet` length (tokens) histogram: `data/output/eda/figures/falcon_main_tweet_len_tokens_hist.png`
- Fallacy label counts bar chart: `data/output/eda/figures/falcon_fallacy_label_counts.png`
- Number of fallacies per tweet histogram: `data/output/eda/figures/falcon_fallacies_per_tweet_hist.png`

## JMBX

**File:** `data/input/unprocessed/jmbx_dataset.csv`

**Number of datapoints (rows):** 1877

### Columns

| Column | Description |
| --- | --- |
| `ID` | Tweet identifier used in the JMBX dataset. |
| `Number of Likes(favor)` | Number of likes (favorites) the tweet received. |
| `Retweet Count` | Number of retweets of the tweet. |
| `Is retweeted` | Whether the tweet is itself a retweet (True/False). |
| `bias` | Political or ideological bias label (e.g. 'lean left', 'right'). |
| `label` | Propaganda technique(s) or rhetorical strategies present in the tweet (list-style string). |
| `slc_label` | Simplified label (e.g. 'propaganda' / 'non-propaganda') summarizing the detailed techniques. |

### Exploratory analysis

**Bias label distribution:**

| Value | Count |
| --- | --- |
| `lean left` | 399 |
| `left` | 398 |
| `right` | 395 |
| `lean right` | 392 |
| `center` | 293 |

**Simplified label (`slc_label`) distribution:**

| Value | Count |
| --- | --- |
| `propaganda` | 1274 |
| `non propaganda` | 603 |

**Number of Likes**

| Metric | Value |
| --- | --- |
| Count | 1877 |
| Min | 0.00 |
| Max | 51584.00 |
| Mean | 278.01 |
| Median | 16.00 |

**Retweet Count**

| Metric | Value |
| --- | --- |
| Count | 1877 |
| Min | 0.00 |
| Max | 49469.00 |
| Mean | 145.49 |
| Median | 5.00 |

- Bias label counts bar chart: `data/output/eda/figures/jmbx_bias_counts.png`
- Simplified label counts bar chart: `data/output/eda/figures/jmbx_slc_label_counts.png`
- Likes histogram: `data/output/eda/figures/jmbx_likes_hist.png`
- Retweet count histogram: `data/output/eda/figures/jmbx_retweets_hist.png`

## MUSE

**File:** `data/input/unprocessed/MUSE_dataset.csv`

**Number of datapoints (rows):** 988

### Columns

| Column | Description |
| --- | --- |
| `created_at` | Timestamp when the note entry was created. |
| `updated_at` | Timestamp when the note entry was last updated. |
| `post_id` | Internal identifier for the post within the dataset. |
| `post_tweet_id` | Original Twitter status ID of the post. |
| `post_text` | Text of the original tweet/post. |
| `response_text` | Text of the explanatory or corrective response (e.g. Community Note / annotation). |
| `response_type` | Source or type of the response (e.g. human-high, human-avg, muse, gpt-4). |
| `annotated` | Whether this datapoint is marked as annotated/valid (e.g. 'Y'). |

### Exploratory analysis

**Length of `post_text` in characters**

| Metric | Value |
| --- | --- |
| Count | 988 |
| Min | 14.00 |
| Max | 280.00 |
| Mean | 164.12 |
| Median | 173.00 |

**Length of `post_text` in tokens**

| Metric | Value |
| --- | --- |
| Count | 988 |
| Min | 3.00 |
| Max | 74.00 |
| Mean | 36.38 |
| Median | 38.00 |

**Length of `response_text` in characters**

| Metric | Value |
| --- | --- |
| Count | 988 |
| Min | 1.00 |
| Max | 1339.00 |
| Mean | 458.36 |
| Median | 427.00 |

**Length of `response_text` in tokens**

| Metric | Value |
| --- | --- |
| Count | 988 |
| Min | 1.00 |
| Max | 366.00 |
| Mean | 108.20 |
| Median | 101.00 |

**Response type distribution (`response_type`):**

| Value | Count |
| --- | --- |
| `human-high` | 247 |
| `human-avg` | 247 |
| `muse` | 247 |
| `gpt-4` | 247 |

**Annotated flag distribution (`annotated`):**

| Value | Count |
| --- | --- |
| `Y` | 941 |
| `N` | 47 |

- `post_text` length (chars) histogram: `data/output/eda/figures/muse_post_text_len_chars_hist.png`
- `response_text` length (chars) histogram: `data/output/eda/figures/muse_response_text_len_chars_hist.png`
- response_type counts bar chart: `data/output/eda/figures/muse_response_type_counts.png`
