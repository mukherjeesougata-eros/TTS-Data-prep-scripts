import csv
from pathlib import Path

#BASE = Path("/data0/Sougata/Dataset/IndicTTS")
OUT = Path("punjabi_fem.tsv")
lang_dir = Path("/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/Sougata/Dataset_l/TTS_data/IndicTTS_l/Punjabi_fem_audio")

rows = []

# Loop over all language folders
# for lang_dir in BASE.iterdir():
#     if not lang_dir.is_dir():
#         continue

    # Find the text file (e.g., Assamese_fem_mono.txt)
# txt_files = list(lang_dir.glob("*.txt"))
# # if not txt_files:
# #     continue
# txt_file = txt_files[0]
txt_file = Path("/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/Sougata/Dataset_l/TTS_data/IndicTTS_l/Punjabi_fem_mono.txt")

    # Find the audio directory (e.g., Assamese_fem_audio)
# audio_dirs = list(lang_dir.glob("*audio"))
# # if not audio_dirs:
# #     continue
# audio_dir = audio_dirs[0]
audio_dir = lang_dir

print(f"Processing {txt_file} ...")

    # Process the .txt transcript file
with open(txt_file, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) < 2:
            continue

        uniq_id_txt, text = parts
        uniq_id = uniq_id_txt.replace(".txt", "")

        # Build wav path
        wav_path = audio_dir / f"{uniq_id}.wav"

        rows.append([uniq_id, text, str(wav_path)])

# Write the consolidated TSV
with open(OUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(rows)

print(f"✔ Finished! Output written to {OUT}")

