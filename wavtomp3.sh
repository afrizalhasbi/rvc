# Convert a dir containing wavs to a dir containing mp3s
# Will use multiprocessing to speed things up
# The new files will have the extensions changed form .wav to .mp3
# Requires ffmpeg

#!/bin/bash

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed. Please install it first."
    exit 1
fi

# Check if a directory path is provided as argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 /path/to/source/folder [number_of_processes]"
    exit 1
fi

# Source directory
SOURCE_DIR="$1"

# Number of parallel processes (default: number of CPU cores)
NUM_PROCESSES=${2:-$(nproc)}

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory does not exist"
    exit 1
fi

# Create destination directory (source_directory_mp3)
DEST_DIR="${SOURCE_DIR%/}_mp3"
mkdir -p "$DEST_DIR"

# Function to convert a single file
convert_file() {
    local file="$1"
    local dest_dir="$2"
    
    # Get filename without path
    local filename=$(basename "$file")
    # Get filename without extension
    local filename_noext="${filename%.*}"
    # Create output filename
    local output_file="$dest_dir/${filename_noext}.mp3"

    echo "Converting: $filename"
    if ffmpeg -i "$file" -codec:a libmp3lame -qscale:a 2 "$output_file" -y 2>/dev/null; then
        echo "Successfully converted: $filename"
        return 0
    else
        echo "Failed to convert: $filename"
        return 1
    fi
}

export -f convert_file

# Find all files and process them in parallel
find "$SOURCE_DIR" -type f -print0 | \
    xargs -0 -I {} -P "$NUM_PROCESSES" \
    bash -c "convert_file \"{}\" \"$DEST_DIR\""

echo "Conversion complete."
echo "Output files are in: $DEST_DIR"
