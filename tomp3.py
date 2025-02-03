import numpy as np
from pydub import AudioSegment
from datasets import load_from_disk, load_dataset

def save_audio_to_mp3(row):
    # Extract audio data and sampling rate
    output_path = f"indah_segments/{row["uid"]}.mp3"
    array = row['audio']["array"]
    sampling_rate = row['audio']["sampling_rate"]

    # Convert normalized float32 audio to int16
    int16_array = (array * 32767).astype(np.int16)

    # Create AudioSegment from numpy array
    audio = AudioSegment(
        data=int16_array.tobytes(),
        sample_width=int16_array.dtype.itemsize,
        frame_rate=sampling_rate,
        channels=1 if array.ndim == 1 else array.shape[1]
    )

    # Export as MP3
    audio.export(output_path, format="mp3")

ds = load_dataset("feedloop-ai/fl-hqfemale-v2")['train']
ds.map(save_audio_to_mp3, num_proc=16, desc="Saving to mp3")
