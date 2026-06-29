# import requests

# headers = {"Authorization": "Bearer hf_your token"}  # your token

# url = "https://datasets-server.huggingface.co/splits?dataset=ai4bharat/Rasa"
# print(requests.get(url, headers=headers).json())
# import requests

# headers = {"Authorization": "Bearer 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"}

# url = "https://datasets-server.huggingface.co/first-rows?dataset=ai4bharat/Rasa&config=default&split=train"

# data = requests.get(url, headers=headers).json()

# for row in data["rows"]:
#     print(row["row"])
# def query():
#     response = requests.get(url, headers=headers)
#     return response.json()
# data = query()
# print(data)
# from datasets import load_dataset

# # Replace 'assamese' with the language/config you want
# # Check available configs on the dataset page
# ds = load_dataset("ai4bharat/Rasa", "Assamese", split="test")

# # Inspect the schema — this shows ALL metadata columns
# #print(ds.features)
# print(ds[0])  # First row with all fields including decoded audio
######################## WORKING WHEN SPLIT IS MENTIONED EXPLICITLY & HAVING DOUBTS WETHER ALL FILES ARE EXTRACTED OR NOT ###############################
# from datasets import load_dataset, Audio, get_dataset_config_names
# import os
# import pandas as pd

# # ---- Config ----
# DATASET_NAME = "ai4bharat/Rasa"
# OUTPUT_BASE = "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/extracted"

# # configs = get_dataset_config_names(DATASET_NAME)
# # print("Available configs:", configs)

# # #for config in configs:
# # print(f"\nProcessing config: {config}")
    
# try:
#     #ds = load_dataset(DATASET_NAME, config, split="train")
#     ds = load_dataset(DATASET_NAME, "Dogri", split="train")
# except Exception as e:
#     print(f"  Skipping {config}: {e}")
# #continue

# # ✅ KEY FIX: disable audio decoding — no torchcodec/soundfile needed
# ds = ds.cast_column("audio", Audio(decode=False))

# #out_dir = os.path.join(OUTPUT_BASE, config, "wavs")
# out_dir = os.path.join(OUTPUT_BASE, "Dogri", "wavs")
# os.makedirs(out_dir, exist_ok=True)

# metadata_rows = []

# for row in ds:
#     audio = row["audio"]

#     # audio["path"] is the original filename from the dataset viewer
#     filename = os.path.basename(audio["path"])

#     # Write raw bytes directly — lossless, no decoding needed
#     out_path = os.path.join(out_dir, filename)
#     with open(out_path, "wb") as f:
#         f.write(audio["bytes"])

#     # Collect all metadata columns except the audio blob
#     meta = {k: v for k, v in row.items() if k != "audio"}
#     meta["audio_filename"] = filename
#     metadata_rows.append(meta)

# # Save metadata CSV
# df = pd.DataFrame(metadata_rows)
# #csv_path = os.path.join(OUTPUT_BASE, config, "metadata.csv")
# csv_path = os.path.join(OUTPUT_BASE, "Dogri", "metadata.csv")
# df.to_csv(csv_path, index=False)

# print(f"  ✅ {len(df)} files extracted → {out_dir}")
# print(f"  ✅ Metadata saved → {csv_path}")
# print(f"  Columns: {list(df.columns)}")
# print(df.head(3))

# 
# from datasets import load_dataset, Audio, get_dataset_config_names, get_dataset_split_names
# import os
# import pandas as pd

# # ---- Config ----
# DATASET_NAME = "CaasiHUANG/InstructTTSEval"
# OUTPUT_BASE = "/mnt/data0/Sougata/Dataset/TTS_data/InstructTTSEval/extracted"

# configs = get_dataset_config_names(DATASET_NAME)
# print("Available configs:", configs)

# for config in configs:
#     print(f"\nProcessing config: {config}")

#     try:
#         splits = get_dataset_split_names(DATASET_NAME, config)
#         print(f"  Splits found: {splits}")
#     except Exception as e:
#         print(f"  Could not get splits for {config}: {e}")
#         continue

#     out_dir = os.path.join(OUTPUT_BASE, config, "wavs")
#     os.makedirs(out_dir, exist_ok=True)

#     metadata_rows = []

#     for split in splits:
#         print(f"  Loading split: {split}")

#         try:
#             ds = load_dataset(DATASET_NAME, config, split=split)
#         except Exception as e:
#             print(f"    Skipping split '{split}': {e}")
#             continue

#         # ✅ Auto-detect audio column name (handles 'audio', 'reference_audio', etc.)
#         audio_col = None
#         for col, feature in ds.features.items():
#             if hasattr(feature, 'decode_example'):  # Audio feature has this
#                 audio_col = col
#                 break

#         if audio_col is None:
#             print(f"    ⚠️  No audio column found. Columns: {list(ds.features.keys())}")
#             continue

#         print(f"    Audio column detected: '{audio_col}'")

#         # ✅ Disable decoding — no torchcodec/FFmpeg needed
#         ds = ds.cast_column(audio_col, Audio(decode=False))

#         for row in ds:
#             audio = row[audio_col]
#             filename = os.path.basename(audio["path"])

#             out_path = os.path.join(out_dir, filename)
#             with open(out_path, "wb") as f:
#                 f.write(audio["bytes"])

#             meta = {k: v for k, v in row.items() if k != audio_col}
#             meta["audio_filename"] = filename
#             meta["split"] = split
#             metadata_rows.append(meta)

#         print(f"    ✅ Split '{split}': {len(ds)} rows")

#     if not metadata_rows:
#         print(f"  ⚠️  No rows collected for config '{config}', skipping CSV.")
#         continue

#     # Save combined metadata CSV for this config
#     df = pd.DataFrame(metadata_rows)
#     csv_path = os.path.join(OUTPUT_BASE, config, "metadata.csv")
#     df.to_csv(csv_path, index=False)

#     print(f"  ✅ Total {len(df)} files extracted → {out_dir}")
#     print(f"  ✅ Metadata saved → {csv_path}")
#     print(f"  Columns: {list(df.columns)}")
#     print(f"  Split breakdown:\n{df['split'].value_counts().to_string()}")
#     print(df.head(3))
from datasets import load_dataset, Audio, get_dataset_config_names, get_dataset_split_names
import os
import pandas as pd

# ---- Config ----
DATASET_NAME = "CaasiHUANG/InstructTTSEval"
OUTPUT_BASE = "/mnt/data0/Sougata/Dataset/TTS_data/InstructTTSEval/extracted"

configs = get_dataset_config_names(DATASET_NAME)
print("Available configs:", configs)

for config in configs:
    print(f"\nProcessing config: {config}")

    try:
        splits = get_dataset_split_names(DATASET_NAME, config)
        print(f"  Splits found: {splits}")
    except Exception as e:
        print(f"  Could not get splits for {config}: {e}")
        continue

    out_dir = os.path.join(OUTPUT_BASE, config, "wavs")
    os.makedirs(out_dir, exist_ok=True)

    metadata_rows = []

    for split in splits:
        print(f"  Loading split: {split}")

        try:
            ds = load_dataset(DATASET_NAME, config, split=split)
        except Exception as e:
            print(f"    Skipping split '{split}': {e}")
            continue

        # Auto-detect audio column
        audio_col = None
        for col, feature in ds.features.items():
            if hasattr(feature, 'decode_example'):
                audio_col = col
                break

        if audio_col is None:
            print(f"    ⚠️  No audio column found. Columns: {list(ds.features.keys())}")
            continue

        print(f"    Audio column detected: '{audio_col}'")
        ds = ds.cast_column(audio_col, Audio(decode=False))

        for idx, row in enumerate(ds):
            audio = row[audio_col]

            # ✅ Handle None path — generate a fallback filename
            raw_path = audio.get("path")
            if raw_path and os.path.basename(raw_path):
                filename = os.path.basename(raw_path)
            else:
                # Fallback: use config + split + index as filename
                filename = f"{config}_{split}_{idx:06d}.wav"

            out_path = os.path.join(out_dir, filename)
            with open(out_path, "wb") as f:
                f.write(audio["bytes"])

            meta = {k: v for k, v in row.items() if k != audio_col}
            meta["audio_filename"] = filename
            meta["split"] = split
            metadata_rows.append(meta)

        print(f"    ✅ Split '{split}': {len(ds)} rows")

    if not metadata_rows:
        print(f"  ⚠️  No rows collected for config '{config}', skipping CSV.")
        continue

    df = pd.DataFrame(metadata_rows)
    csv_path = os.path.join(OUTPUT_BASE, config, "metadata.csv")
    df.to_csv(csv_path, index=False)

    print(f"  ✅ Total {len(df)} files extracted → {out_dir}")
    print(f"  ✅ Metadata saved → {csv_path}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Split breakdown:\n{df['split'].value_counts().to_string()}")
    print(df.head(3))
