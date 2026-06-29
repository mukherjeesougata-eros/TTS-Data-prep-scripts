import os
import pandas as pd

# ---- Config ----
WAV_DIR = "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/extracted/Dogri/wavs"
CSV_PATH = "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/extracted/Dogri/metadata.csv"

# ---- Load data ----
wav_files = set(os.listdir(WAV_DIR))
df = pd.read_csv(CSV_PATH)
csv_files = set(df["audio_filename"].dropna().astype(str))

print(f"Files in wav directory : {len(wav_files)}")
print(f"Filenames in CSV       : {len(csv_files)}")

# ---- Find mismatches ----
in_wav_not_csv = wav_files - csv_files   # present on disk, missing from CSV
in_csv_not_wav = csv_files - wav_files   # present in CSV, missing from disk

print(f"\nIn wav dir but NOT in CSV : {len(in_wav_not_csv)}")
print(f"In CSV but NOT in wav dir : {len(in_csv_not_wav)}")

# ---- Print details ----
if in_wav_not_csv:
    print("\n--- Files on disk but missing from CSV ---")
    for f in sorted(in_wav_not_csv):
        print(f"  {f}")

if in_csv_not_wav:
    print("\n--- Filenames in CSV but missing from disk ---")
    for f in sorted(in_csv_not_wav):
        print(f"  {f}")

# ---- Save mismatches to CSV for reference ----
mismatch_rows = []

for f in sorted(in_wav_not_csv):
    mismatch_rows.append({"audio_filename": f, "present_in_wav_dir": True, "present_in_csv": False})

for f in sorted(in_csv_not_wav):
    mismatch_rows.append({"audio_filename": f, "present_in_wav_dir": False, "present_in_csv": True})

if mismatch_rows:
    mismatch_df = pd.DataFrame(mismatch_rows)
    out_path = "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/extracted/Dogri/mismatches.csv"
    mismatch_df.to_csv(out_path, index=False)
    print(f"\nMismatch report saved to: {out_path}")
else:
    print("\n✅ Perfect match — every wav file has a CSV entry and vice versa.")