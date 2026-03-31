#!/usr/bin/env python3

import csv
import re
from pathlib import Path

# ================= CONFIG =================
WAV_DIR = Path("/mnt/data0/Sougata/Dataset/TTS_data/Rasa/Rasa_extracted/Rasa_renamed")

ROOT_LANG_DIR = Path("/mnt/data0/Sougata/Dataset/TTS_data/Rasa/Rasa_extracted")  # contains language folders + data/
SPLITS = {"train", "test"}

INDICVOICES_ROOT = Path(
    "/mnt/data0/Sougata/Dataset/TTS_data/IndicVoices_r/IndicVoices_extracted"
)

OUTPUT_TSV = Path("Rasa.tsv")
# =========================================


def get_language_code(language: str, split: str) -> str:
    audio_dir = INDICVOICES_ROOT / language / split / "audio"
    if not audio_dir.exists():
        raise RuntimeError(f"IndicVoices audio dir missing: {audio_dir}")

    codes = [d.name for d in audio_dir.iterdir() if d.is_dir()]
    if not codes:
        raise RuntimeError(f"No language_code found for {language}/{split}")

    return codes[0]  # assumed unique


def load_manifest(manifest_csv: Path) -> dict:
    """
    Returns: { sample_id (e.g. sample_12) : third_column_value }
    """
    mapping = {}

    with open(manifest_csv, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue
            mapping[row[0]] = row[2]

    return mapping


def main():
    rows = []

    for language_dir in ROOT_LANG_DIR.iterdir():
        if not language_dir.is_dir():
            continue
        if language_dir.name == "data":
            continue  # 🚫 explicitly skip data folder

        language = language_dir.name

        for split in SPLITS:
            manifest_csv = language_dir / split / f"manifest_{split}.csv"
            if not manifest_csv.exists():
                continue

            language_code = get_language_code(language, split)
            manifest_map = load_manifest(manifest_csv)

            wav_pattern = re.compile(
                rf"Ra_{language_code}_{split}_sample_(\d+)\.wav"
            )

            for wav_path in WAV_DIR.glob("*.wav"):
                match = wav_pattern.fullmatch(wav_path.name)
                if not match:
                    continue

                number = match.group(1)
                sample_id = f"sample_{number}"

                if sample_id not in manifest_map:
                    continue

                rows.append((
                    wav_path.stem,
                    manifest_map[sample_id],
                    str(wav_path.resolve())
                ))

    # Write TSV
    with open(OUTPUT_TSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(rows)

    print(f"✅ TSV written: {OUTPUT_TSV}")
    print(f"🎯 Total rows : {len(rows)}")


if __name__ == "__main__":
    main()

