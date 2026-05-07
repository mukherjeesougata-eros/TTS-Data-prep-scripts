import random

input_tsv = "/mnt/data0/Sougata/Dataset/Nepali_TTS_test/ne_np_female/line_index.tsv"
output_tsv = "test-zipvoice.tsv"
wavs_dir = "/mnt/data0/Sougata/Dataset/Nepali_TTS_test/ne_np_female/wavs"   # change this
random_seed = 42             # set to None for true randomness

if random_seed is not None:
    random.seed(random_seed)

# Read input TSV
rows = []
with open(input_tsv, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        fname, text = line.split("\t")
        rows.append((fname, text))

# Extract texts and shuffle
texts = [text for _, text in rows]
shuffled_texts = texts[:]

# Ensure shuffled text is different per row
while True:
    random.shuffle(shuffled_texts)
    if all(orig != shuf for orig, shuf in zip(texts, shuffled_texts)):
        break

# Write output TSV
with open(output_tsv, "w", encoding="utf-8") as f:
    for (fname, prompt_text), shuffled_text in zip(rows, shuffled_texts):
        wav_name = f"{fname}_syn.wav"
        prompt_wav = f"{wavs_dir}/{fname}.wav"
        f.write(
            f"{wav_name}\t{prompt_text}\t{prompt_wav}\t{shuffled_text}\n"
        )

