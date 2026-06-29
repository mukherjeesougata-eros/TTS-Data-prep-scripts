import pandas as pd

# ---- Config ----
CSV_PATH = "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/extracted/Dogri/metadata.csv"

df = pd.read_csv(CSV_PATH)

actual_rows = len(df)
wc_l_count = sum(1 for _ in open(CSV_PATH, "r", encoding="utf-8"))

print(f"Actual data rows (pandas, correct) : {actual_rows}")
print(f"wc -l equivalent (misleading)      : {wc_l_count - 1}")  # -1 for header
print(f"Difference due to embedded newlines: {wc_l_count - 1 - actual_rows}")