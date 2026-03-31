from pathlib import Path

# ==========================
# INPUT / OUTPUT PATHS
# ==========================
input_tsv = Path("/mnt/data0/Sougata/Dataset/TTS_data/rough/SYSPIN_all_sorted.tsv")          # <-- change this
output_tsv = Path("SYSPIN_all_sorted_wo_0_dur_files.tsv")      # <-- change this

# ==========================
# IDS TO REMOVE
# ==========================
ids_to_remove = {
    "IISc_SYSPINProject_bho_f_SPOR_00056",
    "IISc_SYSPINProject_chha_m_FINA_00364",
    "IISc_SYSPINProject_chha_m_FOOD_01674",
    "IISc_SYSPINProject_hi_m_FINA_01328",
    "IISc_SYSPINProject_mr_m_BOOK_11168",
    "IISc_SYSPINProject_te_f_AGRI_00978",
    "IISc_SYSPINProject_te_f_BOSC_08326",
    "IISc_SYSPINProject_te_f_POLI_00004",
    "IISc_SYSPINProject_te_f_POLI_01290",
}

# ==========================
# FILTER TSV
# ==========================
kept = 0
removed = 0

with input_tsv.open("r", encoding="utf-8") as fin, \
     output_tsv.open("w", encoding="utf-8") as fout:

    for line in fin:
        if not line.strip():
            continue

        file_id = line.split("\t", 1)[0].strip()

        if file_id in ids_to_remove:
            removed += 1
            continue

        fout.write(line)
        kept += 1

print(f"✅ Done")
print(f"Kept   : {kept} lines")
print(f"Removed: {removed} lines")
print(f"Output : {output_tsv}")

