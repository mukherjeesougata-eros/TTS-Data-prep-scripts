python3 - << 'EOF'
import json
from pathlib import Path

root = Path("/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/Sougata/Dataset_l/TTS_data/SYSPIN_2/SYSPIN_extracted/IISc_SYSPIN_Data")

total = 0
for p in root.glob("*/*.json"):
    try:
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        total += len(data.get("Transcripts", {}))
    except Exception as e:
        print(f"[WARN] Skipping {p}: {e}")

print(total)
EOF

