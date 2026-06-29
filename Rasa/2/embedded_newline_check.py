import pandas as pd

# ---- Config ----
CSV_PATH = "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/extracted/Dogri/metadata.csv"
OUT_PATH = "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/extracted/Dogri/embedded_newline_rows.csv"

df = pd.read_csv(CSV_PATH)
print(f"Total rows: {len(df)}")

# ---- Find rows with embedded newlines in ANY column ----
mask = pd.Series([False] * len(df))

for col in df.columns:
    if df[col].dtype == object:
        col_mask = df[col].astype(str).str.contains(r'\n', regex=True, na=False)
        if col_mask.any():
            print(f"  Column '{col}': {col_mask.sum()} rows with embedded newlines")
        mask = mask | col_mask

newline_rows = df[mask]
print(f"\nTotal rows with at least one embedded newline: {len(newline_rows)}")

# ---- Save to separate file ----
newline_rows.to_csv(OUT_PATH, index=False)
print(f"Saved to: {OUT_PATH}")