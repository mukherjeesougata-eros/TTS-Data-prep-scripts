import os
import re
from pathlib import Path

# =====================================================
# CONFIG
# =====================================================
RENAMED_WAV_DIR = (
    "/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/"
    "Sougata/Dataset_l/TTS_data/IndicVoices_r_1/"
    "IndicVoices_extracted/IndicVoices_r_renamed"
)

BASE_EXTRACTED_DIR = (
    "/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/"
    "Sougata/Dataset_l/TTS_data/IndicVoices_r_1/"
    "IndicVoices_extracted"
)

OUT_TSV = "IV_r_6.tsv"

# =====================================================
# WAV FILENAME PATTERN
# =====================================================
wav_pattern = re.compile(
    r"^IV_(?P<lang>[a-z]+)_(?P<split>train|test)_sample_(?P<id>\d{9})\.wav$"
)

# =====================================================
# STEP 1: BUILD TEXT FILE INDEX (ONCE)
# =====================================================
print("🔍 Indexing text files...")

text_index = {}  # key: (lang_code, split, sample_id) → text_path

for language in os.listdir(BASE_EXTRACTED_DIR):
    lang_dir = os.path.join(BASE_EXTRACTED_DIR, language)
    if not os.path.isdir(lang_dir):
        continue

    for split in ("train", "test"):
        text_root = os.path.join(lang_dir, split, "text")
        if not os.path.isdir(text_root):
            continue

        for lang_code in os.listdir(text_root):
            lang_code_dir = os.path.join(text_root, lang_code, split)
            if not os.path.isdir(lang_code_dir):
                continue

            for fname in os.listdir(lang_code_dir):
                if not fname.endswith(".txt"):
                    continue
                if not fname.startswith("sample_"):
                    continue

                sample_id = fname[7:-4]  # sample_XXXXXXXXX.txt
                key = (lang_code, split, sample_id)
                text_index[key] = os.path.join(lang_code_dir, fname)

print(f"✅ Indexed {len(text_index)} text files")

# =====================================================
# STEP 2: PROCESS WAV FILES (FAST LOOKUPS)
# =====================================================
written = 0
skipped = 0

with open(OUT_TSV, "w", encoding="utf-8") as fout:
    for fname in os.listdir(RENAMED_WAV_DIR):
        if not fname.endswith(".wav"):
            continue

        match = wav_pattern.match(fname)
        if not match:
            skipped += 1
            continue

        lang_code = match.group("lang")
        split = match.group("split")
        sample_id = match.group("id")

        key = (lang_code, split, sample_id)
        text_file = text_index.get(key)

        if text_file is None:
            skipped += 1
            continue

        with open(text_file, encoding="utf-8") as f:
            text = f.read().strip().replace("\t", " ").replace("\n", " ")

        uniq_id = fname[:-4]
        wav_path = os.path.join(RENAMED_WAV_DIR, fname)

        fout.write(f"{uniq_id}\t{text}\t{wav_path}\n")
        written += 1

print("✅ TSV creation complete")
print(f"Written : {written}")
print(f"Skipped : {skipped}")
print(f"Output  : {Path(OUT_TSV).resolve()}")

