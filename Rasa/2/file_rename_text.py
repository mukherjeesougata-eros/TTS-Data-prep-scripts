#!/usr/bin/env python3

from pathlib import Path
import shutil

# ================= CONFIG =================
RASA_ROOT = Path(
    "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/Rasa_extracted"
)

INDICVOICES_ROOT = Path(
    "/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/Sougata/Dataset_l/TTS_data/IndicVoices_r_1/IndicVoices_extracted"
)

DEST_DIR = Path("/mnt/data0/Sougata/Dataset/TTS_data/Rasa/Rasa_extracted/Rasa_text_renamed")

SPLITS = {"train", "test"}
# =========================================


def get_language_code(language: str, split: str) -> str | None:
    """
    Extract language_code from IndicVoices structure
    """
    iv_wav_dir = INDICVOICES_ROOT / language / split / "audio"
    if not iv_wav_dir.exists():
        return None

    # Expecting exactly one language_code directory
    codes = [d.name for d in iv_wav_dir.iterdir() if d.is_dir()]
    if not codes:
        return None

    return codes[0]  # use the first (assumed unique)


def main():
    DEST_DIR.mkdir(parents=True, exist_ok=True)

    total = 0
    missing_lang_code = []

    SKIP_DIRS = {"data", "Rasa_renamed", "Rasa_text_renamed"}
    
    for language_dir in RASA_ROOT.iterdir():
        if not language_dir.is_dir():
            continue

        language = language_dir.name
        
        if language in SKIP_DIRS:
            continue
        

        for split_dir in language_dir.iterdir():
            if split_dir.name not in SPLITS:
                continue

            split = split_dir.name

            # Resolve language_code from IndicVoices
            language_code = get_language_code(language, split)
            if language_code is None:
                print(f"⚠️ Missing language_code for {language}/{split}")
                missing_lang_code.append(f"{language}/{split}")
                continue

            rasa_text_dir = (
                split_dir / "text" / language / split
            )
            if not rasa_text_dir.exists():
                continue

            for text_path in rasa_text_dir.glob("*.txt"):
                new_name = f"Ra_{language_code}_{split}_{text_path.name}"
                dest_path = DEST_DIR / new_name

                shutil.copy2(text_path, dest_path)
                total += 1

        print(f"✅ Processed language: {language}")

    print("\n🎯 SUMMARY")
    print(f"Total TEXTs copied : {total}")

    if missing_lang_code:
        print("\n⚠️ Missing language_code for:")
        for x in missing_lang_code:
            print(f"  - {x}")


if __name__ == "__main__":
    main()

