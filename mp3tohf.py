from datasets import load_from_disk
from datasets.features import Audio
import os
import sys

ds_path = sys.argv[1]
audio_dir = sys.argv[2]

ds = load_from_disk(ds_path)
print(ds[0])

ds = ds.remove_columns('audio')

def refunexist(row):
    uid = row['uid']
    return os.path.exists(f"{audio_dir}/{uid}.mp3")

def mapaudio(row):
    uid = row['uid']
    row['audio'] = f"{audio_dir}/{uid}.mp3"
    return row

print(ds)
print("filtering")
ds = ds.filter(refunexist, num_proc=16)
print(ds)
print("mapping audio")
ds = ds.map(mapaudio, num_proc=16)
ds = ds.cast_column('audio', Audio())
print(ds[0])
ds.save_to_disk(ds_path+"_s2t")
