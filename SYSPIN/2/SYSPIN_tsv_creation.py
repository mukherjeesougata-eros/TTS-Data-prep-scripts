import json
from pathlib import Path

# ---------------- CONFIG ----------------
ROOT_DIR = Path(
    "/datasets/ai-core-object/d-gpu-06097851-2053-4b67-8400-b5d404c04261/"
    "Sougata/Dataset_l/TTS_data/SYSPIN_2/SYSPIN_extracted/IISc_SYSPIN_Data"
)
OUT_TSV = "SYSPIN_all.tsv"
# --------------------------------------


def main():
    rows = []
    missing_transcript = 0

    # Iterate over each speaker directory
    for speaker_dir in ROOT_DIR.iterdir():
        if not speaker_dir.is_dir():
            continue

        # Find transcript JSON
        json_files = list(speaker_dir.glob("*_Transcripts.json"))
        if not json_files:
            print(f"[WARN] No transcript JSON in {speaker_dir.name}")
            continue

        transcript_json = json_files[0]

        # Load transcripts
        with open(transcript_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        transcripts = data.get("Transcripts", {})

        # Find wav directory
        wav_dir = speaker_dir / "wav"
        if not wav_dir.exists():
            print(f"[WARN] No wav directory in {speaker_dir.name}")
            continue

        # Iterate over wav files
        for wav_path in wav_dir.glob("*.wav"):
            utt_id = wav_path.stem  # filename without .wav

            if utt_id not in transcripts:
                missing_transcript += 1
                continue

            text = transcripts[utt_id].get("Transcript", "").strip()

            rows.append(
                f"{utt_id}\t{text}\t{wav_path.resolve()}"
            )

    # Write TSV
    with open(OUT_TSV, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(row + "\n")

    print("✅ Manifest generated")
    print(f"Total entries      : {len(rows)}")
    print(f"Missing transcripts: {missing_transcript}")
    print(f"Output written to  : {OUT_TSV}")


if __name__ == "__main__":
    main()

