import os

WAV_DIR = "/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/Sougata/Dataset_l/TTS_data/Rasa/Rasa_extracted/Rasa_renamed"
TXT_DIR = "/mnt/data0/Sougata/Dataset/TTS_data/Rasa/Rasa_extracted/Rasa_text_renamed_2"

print("Sample WAV files:")
for f in os.listdir(WAV_DIR)[:5]:
    print(f)

print("\nSample TXT files:")
for f in os.listdir(TXT_DIR)[:5]:
    print(f)

