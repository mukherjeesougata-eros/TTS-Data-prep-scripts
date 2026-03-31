import json
from pathlib import Path

ROOT = Path(
    "/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/"
    "Sougata/Dataset_l/TTS_data/SYSPIN_2/SYSPIN_extracted/IISc_SYSPIN_Data"
)

total = 0
files = 0

for json_path in ROOT.glob("*/*.json"):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        total += len(data.get("Transcripts", {}))
        files += 1
    except Exception as e:
        print(f"[WARN] Failed to read {json_path}: {e}")

print(f"JSON files processed : {files}")
print(f"Total transcript entries: {total}")

