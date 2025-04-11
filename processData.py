import os
from pathlib import Path

data_dir = Path("dir of your audio data")
output_dir = Path("output dir")

output_dir.mkdir(parents=True, exist_ok=True)

# name the output files
wav_scp_path = output_dir / "audio.scp"
text_scp_path = output_dir / "scripts.txt"

with open(wav_scp_path, "w") as wav_f, open(text_scp_path, "w") as text_f:
    for file in data_dir.glob("*.wav"):
        if file.name.endswith(".wav"):

            prefix = file.stem
            
            wav_path = file.resolve()
            wav_f.write(f"{prefix} {wav_path}\n")
            
            trn_file = file.with_suffix(".wav.trn")
            if trn_file.exists():
                with open(trn_file, "r") as trn_f:

                    target_trn_path = trn_f.readline().strip()

                    target_trn_file = (trn_file.parent / target_trn_path).resolve()
                    if target_trn_file.exists():
                        with open(target_trn_file, "r") as target_trn_f:
                            # read only the audio script in the first line, and ignore the tones in the rest
                            chinese_text = target_trn_f.readline().strip()
                            text_f.write(f"{prefix} {chinese_text}\n")

print(f"Generated {wav_scp_path} and {text_scp_path}")