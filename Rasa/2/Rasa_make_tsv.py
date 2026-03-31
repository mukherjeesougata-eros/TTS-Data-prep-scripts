from pathlib import Path

# ==========================
# CONFIG
# ==========================
WAV_DIR = Path("/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/Sougata/Dataset_l/TTS_data/Rasa/Rasa_extracted/Rasa_renamed")   # <-- change
TXT_DIR = Path("/mnt/data0/Sougata/Dataset/TTS_data/Rasa/Rasa_extracted/Rasa_text_renamed")   # <-- change
OUT_TSV = Path("Rasa_3.tsv")

# ==========================
# BUILD MAPS
# ==========================
wav_files = {p.stem: p for p in WAV_DIR.glob("*.wav")}
txt_files = {p.stem: p for p in TXT_DIR.glob("*.txt")}

common_ids = sorted(wav_files.keys() & txt_files.keys())

missing_wav = txt_files.keys() - wav_files.keys()
missing_txt = wav_files.keys() - txt_files.keys()

# ==========================
# WARNINGS
# ==========================
if missing_wav:
    print(f"⚠ Missing WAV for {len(missing_wav)} IDs")
if missing_txt:
    print(f"⚠ Missing TXT for {len(missing_txt)} IDs")

# ==========================
# WRITE TSV
# ==========================
with OUT_TSV.open("w", encoding="utf-8") as fout:
    for uid in common_ids:
        txt_path = txt_files[uid]
        wav_path = wav_files[uid]

        text = txt_path.read_text(encoding="utf-8").strip().replace("\t", " ")

        fout.write(f"{uid}\t{text}\t{wav_path.resolve()}\n")

print("✅ TSV created")
print(f"Total entries: {len(common_ids)}")
print(f"Output file : {OUT_TSV.resolve()}")

