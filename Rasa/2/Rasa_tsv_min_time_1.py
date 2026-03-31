import os

WAV_DIR = "/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/Sougata/Dataset_l/TTS_data/Rasa/Rasa_extracted/Rasa_renamed"
TXT_DIR = "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/Rasa_extracted/Rasa_text_renamed"
OUT_TSV = "Rasa_5.tsv"

wav_set = {f[:-4] for f in os.listdir(WAV_DIR) if f.endswith(".wav")}

count = 0
with open(OUT_TSV, "w", encoding="utf-8") as out:
    for fname in os.listdir(TXT_DIR):
        if not fname.endswith(".txt"):
            continue

        uid = fname[:-4]
        if uid not in wav_set:
            continue

        txt_path = os.path.join(TXT_DIR, fname)
        wav_path = os.path.join(WAV_DIR, uid + ".wav")

        with open(txt_path, encoding="utf-8") as f:
            text = f.read()

        # 🔑 Normalize text
        text = (
            text.replace("\r\n", " ")
                .replace("\n", " ")
                .replace("\r", " ")
                .replace("\t", " ")
                .strip()
        )

        out.write(f"{uid}\t{text}\t{wav_path}\n")
        count += 1

print("✅ TSV created")
print("Total entries:", count)

