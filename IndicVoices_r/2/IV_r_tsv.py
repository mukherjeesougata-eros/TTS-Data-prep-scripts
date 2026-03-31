from pathlib import Path
import re

# =====================================================
# CONFIG
# =====================================================
RENAMED_WAV_DIR = Path(
    "/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/"
    "Sougata/Dataset_l/TTS_data/IndicVoices_r_1/"
    "IndicVoices_extracted/IndicVoices_r_renamed"
)

BASE_EXTRACTED_DIR = Path(
    "/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/"
    "Sougata/Dataset_l/TTS_data/IndicVoices_r_1/"
    "IndicVoices_extracted"
)

OUT_TSV = Path("IV_r_5.tsv")

# =====================================================
# WAV FILENAME PATTERN
# IV_{lang}_{split}_sample_{9digits}.wav
# =====================================================
wav_pattern = re.compile(
    r"^IV_(?P<lang>[a-z]+)_(?P<split>train|test)_sample_(?P<id>\d{9})\.wav$"
)

# =====================================================
# PROCESS
# =====================================================
written = 0
skipped = 0

with OUT_TSV.open("w", encoding="utf-8") as fout:
    for wav_path in sorted(RENAMED_WAV_DIR.glob("*.wav")):
        fname = wav_path.name
        match = wav_pattern.match(fname)

        if not match:
            skipped += 1
            continue

        lang_code = match.group("lang")
        split = match.group("split")
        sample_id = match.group("id")

        uniq_id = fname[:-4]  # remove .wav

        # -------------------------------------------------
        # Find language directory dynamically
        # Example: Bengali / Hindi / Marathi / Telugu ...
        # -------------------------------------------------
        text_file = None
        for language_dir in BASE_EXTRACTED_DIR.iterdir():
            candidate = (
                language_dir
                / split
                / "text"
                / lang_code
                / split
                / f"sample_{sample_id}.txt"
            )
            if candidate.exists():
                text_file = candidate
                break

        if text_file is None:
            print(f"⚠ Text not found for {uniq_id}")
            skipped += 1
            continue

        # -------------------------------------------------
        # Read text safely
        # -------------------------------------------------
        text = text_file.read_text(encoding="utf-8").strip()
        text = text.replace("\t", " ").replace("\n", " ")

        fout.write(
            f"{uniq_id}\t{text}\t{wav_path.resolve()}\n"
        )
        written += 1

print("✅ TSV creation complete")
print(f"Written : {written}")
print(f"Skipped : {skipped}")
print(f"Output  : {OUT_TSV.resolve()}")

