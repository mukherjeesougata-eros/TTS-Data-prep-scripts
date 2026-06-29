from datasets import load_dataset, get_dataset_config_names, get_dataset_split_names
import os
import pandas as pd

# ---- Config ----
DATASET_NAME = "ajd12342/paraspeechcaps"
OUTPUT_BASE = "/mnt/data0/Sougata/Dataset/TTS_data/ParaSpeechCaps/extracted"

# Exact columns shown in the HuggingFace dataset viewer
EXPECTED_COLUMNS = [
    "source",
    "relative_audio_path",
    "text_description",
    "transcription",
    "intrinsic_tags",
    "situational_tags",
    "basic_tags",
    "all_tags",
    "speakerid",
    "name",
    "duration",
    "gender",
    "accent",
    "pitch",
    "speaking_rate",
    "noise",
    "utterance_pitch_mean",
    "snr",
    "phonemes",
    "tag_of_interest",
]

os.makedirs(OUTPUT_BASE, exist_ok=True)

configs = get_dataset_config_names(DATASET_NAME)
print("Available configs:", configs)

for config in configs:
    print(f"\nProcessing config: {config}")

    try:
        splits = get_dataset_split_names(DATASET_NAME, config)
        print(f"  Splits found: {splits}")
    except Exception as e:
        print(f"  Could not get splits for {config}: {e}")
        continue

    all_dfs = []

    for split in splits:
        print(f"  Loading split: {split} ...")

        try:
            ds = load_dataset(DATASET_NAME, config, split=split)
        except Exception as e:
            print(f"    Skipping split '{split}': {e}")
            continue

        print(f"    Columns in dataset: {list(ds.features.keys())}")

        df = ds.to_pandas()
        df["split"] = split

        # Keep only the expected columns that actually exist, plus split
        cols_present = [c for c in EXPECTED_COLUMNS if c in df.columns]
        missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
        if missing:
            print(f"    Missing columns (will be omitted): {missing}")

        df = df[cols_present + ["split"]]

        # Flatten list-type columns to semicolon-separated strings for CSV readability
        for col in df.columns:
            if df[col].dtype == object and df[col].map(lambda x: isinstance(x, list)).any():
                df[col] = df[col].map(lambda x: "; ".join(str(i) for i in x) if isinstance(x, list) else x)

        all_dfs.append(df)
        print(f"    Split '{split}': {len(df)} rows, {len(cols_present)} columns")

    if not all_dfs:
        print(f"  No data collected for config '{config}', skipping.")
        continue

    combined = pd.concat(all_dfs, ignore_index=True)

    config_dir = os.path.join(OUTPUT_BASE, config)
    os.makedirs(config_dir, exist_ok=True)
    csv_path = os.path.join(config_dir, "metadata.csv")
    combined.to_csv(csv_path, index=False)

    print(f"\n  Metadata saved → {csv_path}")
    print(f"  Total rows : {len(combined)}")
    print(f"  Columns    : {list(combined.columns)}")
    print(f"  Split breakdown:\n{combined['split'].value_counts().to_string()}")
    print(combined.head(3).to_string())
