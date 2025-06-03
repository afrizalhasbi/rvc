import os
from datasets import load_from_disk, load_dataset
import soundfile as sf
import sys
import librosa
import gc
from tqdm import tqdm
import uuid

def save_audio_to_mp3(example):
    # gc.collect()
    try:
        os.makedirs(f'{save_dir}_mp3', exist_ok=True)
        audio_array = example['audio']['array']
        src_sr = example['audio']['sampling_rate']
        uid = example['uid']
        output_path = f'{save_dir}_mp3/{uid}.mp3'
        if os.path.exists(output_path):
            return example

        target_sr = 44100
        if src_sr != target_sr:
            audio_array = librosa.resample(audio_array, orig_sr=src_sr, target_sr=target_sr)

        sf.write(output_path, audio_array, target_sr, format='mp3')
        return example
    except Exception as e:
        print(f"Got error: {e}")
        return example

def free_ds(example):
    uid = example['uid']
    output_path = f'{save_dir}_mp3/{uid}.mp3'
    # print(output_path)
    return not os.path.exists(output_path)

dataset_name = sys.argv[1]
save_dir = sys.argv[2]
output_path = f'{save_dir}_mp3'

print(output_path)


# ds = load_dataset(dataset_name, split='train')
ds = load_from_disk(dataset_name)

# print("=========one==========")
# print(ds)
# ds = ds.filter(free_ds, num_proc=12, desc="Filtering")

# print("=========two==========")
print(ds)
div_at = len(ds) // 2
ds.select(range(div_at)).map(save_audio_to_mp3, num_proc=1, desc="Save to mp3")
gc.collect()
ds.select(range(div_at, len(ds))).map(save_audio_to_mp3, num_proc=1, desc="Save to mp3")
