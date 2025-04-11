import os
from pydub import AudioSegment


data_dir = "dir of your clean voice data"
noise_file = "path to your noise file"


noise = AudioSegment.from_wav(noise_file)

for filename in os.listdir(data_dir):
    if filename.endswith('.wav') and not filename.endswith('.wav.trn'):
        file_path = os.path.join(data_dir, filename)
        print(f'processing file {filename}')
        
        audio = AudioSegment.from_wav(file_path)
        
        repeated_noise = noise
        while len(repeated_noise) < len(audio):
            repeated_noise += noise
        
        noise_segment = repeated_noise[:len(audio)]
        
        mixed = audio.overlay(noise_segment)
        
        mixed.export(file_path, format='wav')
        print(f'saved as {filename}')

print("All wav files processed.")
