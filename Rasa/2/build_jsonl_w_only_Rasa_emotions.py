import csv
import json
import os

ROOT = "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/extracted"
OUT_TRAIN = os.path.join(ROOT, "rasa_emotions_train.jsonl")
OUT_TEST = os.path.join(ROOT, "rasa_emotions_test.jsonl")

LANG_ID = {
    "Assamese": "as", "Bengali": "bn", "Bodo": "brx", "Dogri": "dgo",
    "Gujarati": "gu", "Hindi": "hi", "Kannada": "kn", "Kashmiri": "ks",
    "Konkani": "knn", "Maithili": "mai", "Malayalam": "ml", "Manipuri": "mni",
    "Marathi": "mr", "Nepali": "npi", "Odia": "ory", "Punjabi": "pa",
    "Sanskrit": "sa", "Santali": "sat", "Sindhi": "sd", "Tamil": "ta",
    "Telugu": "te", "Urdu": "ur",
}

STYLES = {"HAPPY", "SAD", "ANGER", "FEAR", "DISGUST", "SURPRISE"}

per_lang = {}
per_style = {}
per_split = {"train": 0, "test": 0, "other": 0}

with open(OUT_TRAIN, "w", encoding="utf-8") as f_train, \
     open(OUT_TEST, "w", encoding="utf-8") as f_test:

    for lang in sorted(LANG_ID):
        csv_path = os.path.join(ROOT, lang, "metadata.csv")
        if not os.path.isfile(csv_path):
            print(f"[skip] missing {csv_path}")
            continue
        count = 0
        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                style = (row.get("style") or "").strip().upper()
                if style not in STYLES:
                    continue
                audio_filename = (row.get("audio_filename") or "").strip()
                if not audio_filename:
                    continue
                split = (row.get("split") or "").strip().lower()
                file_id = os.path.splitext(audio_filename)[0]
                audio_path = os.path.join(ROOT, lang, "wavs", audio_filename)
                obj = {
                    "id": file_id,
                    "audio_path": audio_path,
                    "text": (row.get("text") or "").strip(),
                    "instruct": style.lower(),
                    "language_id": LANG_ID[lang],
                }
                line = json.dumps(obj, ensure_ascii=False) + "\n"
                if split == "train":
                    f_train.write(line)
                    per_split["train"] += 1
                elif split == "test":
                    f_test.write(line)
                    per_split["test"] += 1
                else:
                    per_split["other"] += 1
                    continue
                count += 1
                per_style[style] = per_style.get(style, 0) + 1
        per_lang[lang] = count

print(f"Train rows: {per_split['train']}  ->  {OUT_TRAIN}")
print(f"Test rows : {per_split['test']}  ->  {OUT_TEST}")
if per_split["other"]:
    print(f"Skipped (unknown split): {per_split['other']}")
print("Per-language counts:")
for lang in sorted(per_lang):
    print(f"  {lang:12s} {per_lang[lang]}")
print("Per-style counts:")
for s in sorted(per_style):
    print(f"  {s:10s} {per_style[s]}")
