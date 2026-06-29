"""
Pairs ParaSpeechCaps metadata with Emilia audio files.

Output per config:
  OUTPUT_BASE/<config>/wavs/         ← matched .mp3 files
  OUTPUT_BASE/<config>/metadata.csv  ← all 20 metadata columns + audio_filename + split

Requirements:
  pip install datasets pandas tqdm

Authentication:
  Both datasets may require a HuggingFace account and accepted terms.
  Set your token before running:
    export HF_TOKEN="hf_..."
"""

import os
import pandas as pd
from datasets import load_dataset, get_dataset_config_names, get_dataset_split_names
from tqdm import tqdm

# ── Config ────────────────────────────────────────────────────────────────────
PARASPEECHCAPS = "ajd12342/paraspeechcaps"
EMILIA         = "amphion/Emilia-Dataset"
OUTPUT_BASE    = "/mnt/f2fee9b0-4d49-4f00-ab25-c03e91e4cc6e/ParaSpeechCaps/extracted"
HF_TOKEN       = os.environ.get("HF_TOKEN")          # export HF_TOKEN="hf_..."

METADATA_COLUMNS = [
    "source", "relative_audio_path", "text_description", "transcription",
    "intrinsic_tags", "situational_tags", "basic_tags", "all_tags",
    "speakerid", "name", "duration", "gender", "accent", "pitch",
    "speaking_rate", "noise", "utterance_pitch_mean", "snr", "phonemes",
    "tag_of_interest",
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def flatten_lists(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten list-type columns to semicolon-separated strings for CSV."""
    for col in df.columns:
        if df[col].dtype == object and df[col].map(lambda x: isinstance(x, list)).any():
            df[col] = df[col].map(
                lambda x: "; ".join(str(i) for i in x) if isinstance(x, list) else x
            )
    return df


def get_mp3_bytes(record: dict) -> bytes | None:
    """
    Extract raw MP3 bytes from an Emilia WebDataset record.
    The 'mp3' field can be raw bytes or a HuggingFace Audio dict.
    """
    mp3 = record.get("mp3")
    if mp3 is None:
        return None
    if isinstance(mp3, bytes):
        return mp3
    if isinstance(mp3, dict):
        return mp3.get("bytes")
    return None


def emilia_keys(record: dict) -> list[str]:
    """
    Return candidate lookup keys from an Emilia record.
    Emilia __key__ can be:
      - base filename only:   EN_B00030_S01984_W000037
      - full relative path:   EN/EN_B00030/EN_B00030_S01984/mp3/EN_B00030_S01984_W000037
    We return both so we can match against whichever form ParaSpeechCaps uses.
    """
    raw = record.get("__key__", "")
    if not raw:
        return []
    base = os.path.basename(raw)
    keys = [raw, base]
    # Also try with .mp3 extension in case paths stored with extension
    keys += [raw + ".mp3", base + ".mp3"]
    return keys


# ── Step 1: Load all ParaSpeechCaps metadata ──────────────────────────────────
print("=" * 65)
print("STEP 1  Loading ParaSpeechCaps metadata")
print("=" * 65)

configs = get_dataset_config_names(PARASPEECHCAPS)
print(f"Configs found: {configs}\n")

# Two lookup tables to handle both __key__ formats from Emilia
# key_to_meta maps:  lookup_key  →  {"config": str, "meta": dict}
key_to_meta_full = {}   # relative_audio_path without extension
key_to_meta_base = {}   # basename without extension

config_rows: dict[str, list[dict]] = {cfg: [] for cfg in configs}

for config in configs:
    print(f"Config: {config}")
    try:
        splits = get_dataset_split_names(PARASPEECHCAPS, config)
        print(f"  Splits: {splits}")
    except Exception as e:
        print(f"  Skipping — cannot list splits: {e}")
        continue

    for split in splits:
        print(f"  Loading '{split}' ...")
        try:
            ds = load_dataset(PARASPEECHCAPS, config, split=split, token=HF_TOKEN)
        except Exception as e:
            print(f"  Skipping '{split}': {e}")
            continue

        for row in tqdm(ds, desc=f"  {config}/{split}", unit="rows"):
            rap = row.get("relative_audio_path", "")
            if not rap:
                continue

            full_key = os.path.splitext(rap)[0]                    # EN/EN_B00030/.../EN_B00030_S01984_W000037
            base_key = os.path.splitext(os.path.basename(rap))[0]  # EN_B00030_S01984_W000037

            meta_row = {k: row[k] for k in METADATA_COLUMNS if k in row}
            meta_row["split"] = split
            entry = {"config": config, "meta": meta_row}

            key_to_meta_full[full_key] = entry
            key_to_meta_base[base_key] = entry
            config_rows[config].append(meta_row)

total_keys = len(key_to_meta_base)
print(f"\nTotal unique audio entries: {total_keys:,}")

# ── Step 2: Prepare output directories ───────────────────────────────────────
for config in configs:
    os.makedirs(os.path.join(OUTPUT_BASE, config, "wavs"), exist_ok=True)

# Resume support: detect already-saved files
saved_base_keys: set[str] = set()
for config in configs:
    wavs_dir = os.path.join(OUTPUT_BASE, config, "wavs")
    for fname in os.listdir(wavs_dir):
        bk = os.path.splitext(fname)[0]
        if bk in key_to_meta_base:
            saved_base_keys.add(bk)

print(f"Already saved (resume): {len(saved_base_keys):,} / {total_keys:,}")
remaining = total_keys - len(saved_base_keys)
print(f"Remaining to download : {remaining:,}")

# ── Step 3: Stream Emilia and save matching audio ─────────────────────────────
if remaining > 0:
    print("\n" + "=" * 65)
    print("STEP 2  Streaming Emilia — saving matched audio")
    print("=" * 65)
    print("NOTE: Emilia is a large dataset. This may take several hours.")
    print("      The script supports resuming — re-run to continue.\n")

    try:
        emilia = load_dataset(EMILIA, split="train", streaming=True, token=HF_TOKEN)
    except Exception as e:
        print(f"ERROR loading Emilia: {e}")
        print("Make sure you have accepted the Emilia terms on HuggingFace")
        print("and that HF_TOKEN is set correctly.")
        raise

    newly_saved = 0
    scanned = 0

    for record in tqdm(emilia, desc="Scanning Emilia", unit="records"):
        scanned += 1
        candidates = emilia_keys(record)

        # Find which lookup key matches
        matched_entry = None
        matched_base  = None
        for ck in candidates:
            if ck in key_to_meta_full:
                matched_entry = key_to_meta_full[ck]
                matched_base  = os.path.basename(ck)
                break
            if ck in key_to_meta_base:
                matched_entry = key_to_meta_base[ck]
                matched_base  = ck
                break

        if matched_entry is None:
            continue

        # Strip any .mp3 suffix that snuck in from the candidates list
        if matched_base and matched_base.endswith(".mp3"):
            matched_base = matched_base[:-4]

        if matched_base in saved_base_keys:
            continue   # already saved in a previous run

        mp3_bytes = get_mp3_bytes(record)
        if not mp3_bytes:
            continue

        config   = matched_entry["config"]
        out_path = os.path.join(OUTPUT_BASE, config, "wavs", f"{matched_base}.mp3")

        with open(out_path, "wb") as f:
            f.write(mp3_bytes)

        saved_base_keys.add(matched_base)
        newly_saved += 1

        if newly_saved % 5_000 == 0:
            print(f"\n  Saved {newly_saved:,} new files  "
                  f"(total matched {len(saved_base_keys):,} / {total_keys:,}, "
                  f"scanned {scanned:,} Emilia records)")

        if len(saved_base_keys) >= total_keys:
            print("\n  All keys matched — stopping Emilia stream early.")
            break

    unmatched = total_keys - len(saved_base_keys)
    print(f"\nEmilia scan complete.")
    print(f"  Newly saved  : {newly_saved:,}")
    print(f"  Total matched: {len(saved_base_keys):,} / {total_keys:,}")
    if unmatched:
        print(f"  Not found    : {unmatched:,}  (these keys had no match in Emilia)")
else:
    print("\nAll audio already downloaded. Skipping Emilia stream.")

# ── Step 4: Save metadata CSVs ────────────────────────────────────────────────
print("\n" + "=" * 65)
print("STEP 3  Saving metadata CSVs")
print("=" * 65)

for config, rows in config_rows.items():
    if not rows:
        print(f"  Config '{config}': no rows — skipping.")
        continue

    df = pd.DataFrame(rows)
    df = flatten_lists(df)

    # Add audio_filename column pointing to the saved .mp3 in wavs/
    df["audio_filename"] = df["relative_audio_path"].map(
        lambda rap: os.path.splitext(os.path.basename(rap))[0] + ".mp3"
        if isinstance(rap, str) and rap else ""
    )

    # Column order: audio_filename first, then all metadata columns, then split
    ordered = ["audio_filename"] + [c for c in METADATA_COLUMNS if c in df.columns] + ["split"]
    df = df[[c for c in ordered if c in df.columns]]

    csv_path = os.path.join(OUTPUT_BASE, config, "metadata.csv")
    df.to_csv(csv_path, index=False)

    print(f"\n  Config : {config}")
    print(f"  Rows   : {len(df):,}")
    print(f"  CSV    : {csv_path}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Splits :\n{df['split'].value_counts().to_string()}")
    print(df.head(3).to_string())

print("\n\nAll done!")
print(f"Output root: {OUTPUT_BASE}")
