from pathlib import Path

ROOT = Path("/mnt/data0/Sougata/Dataset/TTS_data/Rasa/Rasa_extracted")

empty_files = []

for txt in ROOT.rglob("*.txt"):
    # Skip any path that contains /data/
    if "data" in txt.parts:
        continue

    # Check empty or whitespace-only
    if txt.stat().st_size == 0:
        empty_files.append(txt)
    else:
        content = txt.read_text(encoding="utf-8", errors="ignore").strip()
        if content == "":
            empty_files.append(txt)

# Report
print(f"Total empty .txt files: {len(empty_files)}")
for f in empty_files:
    print(f)

