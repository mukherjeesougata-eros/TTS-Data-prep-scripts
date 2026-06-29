from datasets import load_dataset

# Load English subset
dataset_en = load_dataset("CaasiHUANG/InstructTTSEval", split="en")

# Load Chinese subset  
dataset_zh = load_dataset("CaasiHUANG/InstructTTSEval", split="zh")

# Load both languages
dataset = load_dataset("CaasiHUANG/InstructTTSEval")
english_data = dataset["en"]
chinese_data = dataset["zh"]

# Verify splits
print("Available splits:", list(dataset.keys()))  # Should show ['en', 'zh']

# Access audio data (automatically loaded from embedded Parquet)
example = dataset_en[0]
print(f"Text: {example['text']}")
print(f"Audio sampling rate: {example['reference_audio']['sampling_rate']}")
print(f"Audio array shape: {example['reference_audio']['array'].shape}")

# Play audio (if using jupyter/colab)
import IPython.display as ipd
ipd.Audio(example['reference_audio']['array'], rate=example['reference_audio']['sampling_rate'])
