#!/usr/bin/env python3

import os
import sys
import argparse
import traceback

import numpy as np
import soundfile as sf
import torch
from io import BytesIO

# Make sure you can import from your RVC repo:
# e.g. put 'modules.py' + 'pipeline.py' + 'utils.py' etc. in a folder called "rvc_infer"
# or adjust the path below so that Python finds them
# For example:
# from rvc_infer.modules import VC
# from rvc_infer.lib.audio import load_audio, wav2
#
# In this snippet, I'll assume you have them in the same directory or a proper package.

print("Importing config")
from configs.config import Config
print("Importing VC")
from infer.modules.vc.modules import VC
print("Importing infer.lib.audio")
from infer.lib.audio import load_audio, wav2
print("All imports successful")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Simple RVC batch inference script.")
    parser.add_argument(
        "--model_path",
        type=str,
        required=True,
        help="Path to the .pth RVC model file. Example: /home/ubuntu/weights/MyModel.pth",
    )
    parser.add_argument(
        "--input_dir",
        type=str,
        required=True,
        help="Path to the folder containing input audio files.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="converted_output",
        help="Folder to store the converted audio files. Default='converted_output'",
    )
    parser.add_argument(
        "--f0_up_key",
        type=int,
        default=0,
        help="Integer pitch shift (semitones). Example: 12 = up one octave, -12 = down one octave. Default=0",
    )
    parser.add_argument(
        "--f0_method",
        type=str,
        default="rmvpe",
        choices=["pm", "harvest", "dio", "crepe", "rmvpe", "rmvpe_gpu"],
        help="Method to extract f0. Default='rmvpe'",
    )
    parser.add_argument(
        "--file_index",
        type=str,
        default="",
        help="Optional: path to your .index file for retrieval-based style. Leave blank if none.",
    )
    parser.add_argument(
        "--index_rate",
        type=float,
        default=1.0,
        help="How much to rely on the index features (0 to 1). Default=1.0",
    )
    parser.add_argument(
        "--filter_radius",
        type=int,
        default=3,
        help="Median filtering radius for harvest f0, can help remove 'choppy' artifacts. 0 to 7. Default=3",
    )
    parser.add_argument(
        "--resample_sr",
        type=int,
        default=0,
        help="Final resample rate (e.g. 22050, 44100, 48000). 0 = no resampling. Default=0",
    )
    parser.add_argument(
        "--rms_mix_rate",
        type=float,
        default=0.25,
        help="Crossfade ratio of source-loudness envelope vs. output-loudness envelope. Default=0.25",
    )
    parser.add_argument(
        "--protect",
        type=float,
        default=0.33,
        help="Protect range for unvoiced/low-energy segments to reduce metallic artifacts. 0 to 0.5. Default=0.33",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="mp3",
        choices=["wav", "flac", "m4a", "mp3"],
        help="Output audio format. Default=wav",
    )
    parser.add_argument(
        "--skip_existing",
        action="store_true",
        help="If specified, will skip conversion if output file already exists in output_dir",
    )
    return parser.parse_args()

def main():
    try:
        args = parse_arguments()
        # Create config object
        print("Initializing config")
        config = Config()
        print("Initializing config succesfull")
        config.device = "cuda:0"
        config.is_half = True     # if you have enough GPU memory, half can speed things up
    
        # 1) Initialize VC object
        vc = VC(config)
    
        # 2) Trick: the original `vc.get_vc(sid)` expects a 'sid' that is the name of the .pth
        #    in your weights folder. By default, it does something like:
        #        person = f'{os.getenv("weight_root")}/{sid}'
        #
        #    If you want to just feed it a full path, you can do:
        #      os.environ["weight_root"] = ""    # or something else
        #      sid = args.model_path
        #
        #    Or, you can patch `get_vc` yourself. For simplicity, let's do:
        print("Get weight_root")
        os.environ["weight_root"] = os.path.dirname(args.model_path)
        sid_basename = os.path.basename(args.model_path)
        print(f"Model path: {args.model_path}")
        print(f"SID basename path: {sid_basename}")
    
        # 3) Actually load the model
        #    This will set up the pipeline, net_g, etc.
        vc.get_vc(sid_basename)
    
        # 4) Gather all input audio paths
        input_files = []
        if not os.path.isdir(args.input_dir):
            print(f"ERROR: input_dir={args.input_dir} is not a directory.")
            sys.exit(1)
        for fname in os.listdir(args.input_dir):
            # optionally filter by extension
            if fname.lower().endswith((".wav", ".mp3", ".flac", ".ogg", ".m4a")):
                input_files.append(os.path.join(args.input_dir, fname))
        input_files.sort()
    
        # 5) Make sure output directory is ready
        os.makedirs(args.output_dir, exist_ok=True)
    
        # 6) For each file, run single-file inference and write
        for in_path in input_files:
            # Build output path: e.g. "my_audio.mp3.wav" or "my_audio.wav.flac" etc
            out_name = f"{os.path.basename(in_path)}.{args.format}"
            out_path = os.path.join(args.output_dir, out_name)
    
            if args.skip_existing and os.path.exists(out_path):
                print(f"[INFO] Skipping existing: {out_path}")
                continue
    
            print(f"[INFO] Converting: {in_path} -> {out_path}")
            try:
                # call vc_single
                info, (tgt_sr, audio_opt) = vc.vc_single(
                    # sid_basename,
                    0,
                    in_path,
                    f0_up_key=args.f0_up_key,
                    f0_file=None,        # not using external f0 file
                    f0_method=args.f0_method,
                    file_index=args.file_index,
                    file_index2="",      # we won't handle file_index2 here
                    index_rate=args.index_rate,
                    filter_radius=args.filter_radius,
                    resample_sr=args.resample_sr,
                    rms_mix_rate=args.rms_mix_rate,
                    protect=args.protect,
                )
    
                if "Success" not in info or (tgt_sr is None or audio_opt is None):
                    # means some error occurred in vc_single
                    print(f"[WARNING] Inference failed on {in_path}\n{info}")
                    continue
    
                # Write to disk
                if args.format in ["wav", "flac"]:
                    sf.write(out_path, audio_opt, tgt_sr, format=args.format)
                else:
                    # for mp3/m4a etc. we do the same “in-memory wav then encode” approach
                    from infer.lib.audio import wav2
                    with BytesIO() as wav_buffer:
                        sf.write(wav_buffer, audio_opt, tgt_sr, format="wav")
                        wav_buffer.seek(0)
                        with open(out_path, "wb") as outf:
                            wav2(wav_buffer, outf, args.format)
    
                print(f"[INFO] Done: {in_path} -> {out_path}")
            except Exception as e:
                traceback.print_exc()
                print(f"[ERROR] Failed on {in_path}: {str(e)}")
    
        print("All done!")
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
