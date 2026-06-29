# import requests

# headers = {"Authorization": "Bearer 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"}  # your token

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

from datasets import load_dataset, Audio, get_dataset_config_names, get_dataset_split_names
import os
import pandas as pd

# ---- Config ----
DATASET_NAME = "ai4bharat/Rasa"
OUTPUT_BASE = "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/extracted"

configs = get_dataset_config_names(DATASET_NAME)
print("Available configs:", configs)

for config in configs:
    print(f"\nProcessing config: {config}")

    try:
        splits = get_dataset_split_names(DATASET_NAME, config)
        #splits = get_dataset_split_names(DATASET_NAME, "Dogri")
        print(f"  Splits found: {splits}")
    except Exception as e:
        print(f"  Could not get splits for {config}: {e}")
        continue

    out_dir = os.path.join(OUTPUT_BASE, config, "wavs")
    #out_dir = os.path.join(OUTPUT_BASE, "Dogri", "wavs")
    os.makedirs(out_dir, exist_ok=True)

    metadata_rows = []

    for split in splits:
        print(f"  Loading split: {split}")

        try:
            ds = load_dataset(DATASET_NAME, config, split=split)
            #ds = load_dataset(DATASET_NAME, "Dogri", split=split)
        except Exception as e:
            print(f"    Skipping split '{split}': {e}")
            continue

        ds = ds.cast_column("audio", Audio(decode=False))

        for row in ds:
            audio = row["audio"]
            filename = os.path.basename(audio["path"])

            out_path = os.path.join(out_dir, filename)
            with open(out_path, "wb") as f:
                f.write(audio["bytes"])

            meta = {k: v for k, v in row.items() if k != "audio"}
            meta["audio_filename"] = filename
            meta["split"] = split          # track which split this row came from
            metadata_rows.append(meta)

        print(f"    ✅ Split '{split}': {len(ds)} rows")

    # Save combined metadata CSV for this config
    df = pd.DataFrame(metadata_rows)
    csv_path = os.path.join(OUTPUT_BASE, config, "metadata.csv")
    #csv_path = os.path.join(OUTPUT_BASE, "Dogri", "metadata.csv")
    df.to_csv(csv_path, index=False)

    print(f"  ✅ Total {len(df)} files extracted → {out_dir}")
    print(f"  ✅ Metadata saved → {csv_path}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Split breakdown:\n{df['split'].value_counts().to_string()}")
    print(df.head(3))
