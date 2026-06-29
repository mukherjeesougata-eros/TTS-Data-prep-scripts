# import pandas as pd

# df = pd.read_csv("/mnt/data0/Sougata/Dataset/TTS_data/Rasa/extracted/Dogri/metadata.csv")
# print("Total rows:", len(df))
# print("Unique filenames:", df["audio_filename"].nunique())
# print("Duplicated filenames:", df["audio_filename"].duplicated().sum())

# # See which filenames are duplicated
# dupes = df[df["audio_filename"].duplicated(keep=False)]
# print(dupes[["audio_filename"]].sort_values("audio_filename").head(20))
import pandas as pd
import sys

# ---- Config ----
CSV_PATH = "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/extracted/Dogri/metadata.csv"  # Change this to your CSV path

df = pd.read_csv(CSV_PATH)

print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Columns: {list(df.columns)}\n")

# ---- 1. Fully duplicate rows (every column identical) ----
full_dupes = df[df.duplicated(keep=False)]
print(f"Fully duplicate rows (all columns match): {df.duplicated().sum()}")
if not full_dupes.empty:
    print(full_dupes.head(10))

print()

# ---- 2. Duplicate audio filenames ----
if "audio_filename" in df.columns:
    fname_dupes = df[df["audio_filename"].duplicated(keep=False)]
    print(f"Duplicate audio_filename values: {df['audio_filename'].duplicated().sum()}")
    if not fname_dupes.empty:
        print(fname_dupes[["audio_filename", "split"] if "split" in df.columns else ["audio_filename"]]
              .sort_values("audio_filename").head(20))
    print()

# ---- 3. Per-column duplicate check ----
print("Per-column duplicate counts:")
for col in df.columns:
    n_dupes = df[col].duplicated().sum()
    n_unique = df[col].nunique()
    print(f"  {col:<40} dupes: {n_dupes:<8} unique: {n_unique}")

print()

# ---- 4. Save duplicate rows to a separate CSV for inspection ----
if not full_dupes.empty:
    out_path = CSV_PATH.replace(".csv", "_duplicates.csv")
    full_dupes.to_csv(out_path, index=False)
    print(f"Duplicate rows saved to: {out_path}")
else:
    print("No fully duplicate rows found — CSV is clean.")

# Find which column(s) contain embedded newlines
for col in df.columns:
    if df[col].dtype == object:
        mask = df[col].astype(str).str.contains(r'\n', regex=True, na=False)
        if mask.any():
            print(f"Column '{col}' has {mask.sum()} rows with embedded newlines")
            print("Example:", repr(df[col][mask].iloc[0]))