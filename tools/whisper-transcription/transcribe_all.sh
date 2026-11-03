#!/bin/bash

# Script to transcribe all Hebrew lecture videos using whisper.cpp
# Optimized for Apple Silicon (M-series processors)

# Set paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="${BASE_DIR:-$SCRIPT_DIR}"
INPUT_DIR="$BASE_DIR/Input"
OUTPUT_DIR="$BASE_DIR/output"
WHISPER_DIR="$BASE_DIR/whisper.cpp"
MODEL_PATH="$WHISPER_DIR/models/ggml-large-v3.bin"
WHISPER_CLI="$WHISPER_DIR/build/bin/whisper-cli"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to transcribe a single video
transcribe_video() {
    local video_path="$1"
    local video_name=$(basename "$video_path")
    local video_dir=$(dirname "$video_path")
    local folder_name=$(basename "$video_dir")
    
    # Remove file extension
    local base_name="${video_name%.*}"
    
    # Create output subdirectory for this course folder
    local course_output_dir="$OUTPUT_DIR/$folder_name"
    mkdir -p "$course_output_dir"
    
    # Create temp directory for audio extraction
    local temp_dir="$BASE_DIR/temp_audio"
    mkdir -p "$temp_dir"
    
    local temp_audio="$temp_dir/${base_name}.wav"
    
    echo "=========================================="
    echo "Transcribing: $video_name"
    echo "Course: $folder_name"
    echo "=========================================="
    
    # Extract audio from video using ffmpeg
    echo "Extracting audio from video..."
    ffmpeg -i "$video_path" -ar 16000 -ac 1 -c:a pcm_s16le "$temp_audio" -y 2>&1
    
    if [ $? -ne 0 ] || [ ! -f "$temp_audio" ]; then
        echo "✗ Failed to extract audio from: $video_name"
        echo "FFmpeg error occurred. Check video file integrity."
        return 1
    fi
    
    echo "Audio extracted successfully. Starting transcription..."
    
    # Run whisper with Hebrew language and optimized settings for Apple Silicon
    # -l he: Hebrew language
    # -m: model path
    # -f: input file
    # -of: output filename (without extension)
    # -otxt: output text file
    # -osrt: output SRT file with timestamps
    # -ovtt: output VTT file with timestamps
    # -t 8: use 8 threads (good for M-series)
    # --processors 1: use 1 processor for audio processing
    # --split-on-word: split on word for better timestamp accuracy
    
    DYLD_LIBRARY_PATH="$WHISPER_DIR/build/src:$WHISPER_DIR/build/ggml/src:$WHISPER_DIR/build/ggml/src/ggml-blas:$WHISPER_DIR/build/ggml/src/ggml-metal" "$WHISPER_CLI" \
        -l he \
        -m "$MODEL_PATH" \
        -f "$temp_audio" \
        -of "$course_output_dir/$base_name" \
        -otxt \
        -osrt \
        -ovtt \
        -t 8 \
        --processors 1 \
        --split-on-word \
        --max-len 30 \
        --temperature 0.0
    
    local whisper_status=$?
    
    # Clean up temporary audio file
    rm -f "$temp_audio"
    
    if [ $whisper_status -eq 0 ]; then
        echo "✓ Successfully transcribed: $video_name"
        echo "  Output files:"
        echo "  - $course_output_dir/$base_name.txt"
        echo "  - $course_output_dir/$base_name.srt"
        echo "  - $course_output_dir/$base_name.vtt"
    else
        echo "✗ Failed to transcribe: $video_name"
    fi
    echo ""
}

# Find and transcribe all video files in Input directory
echo "Starting transcription of all Hebrew lecture videos..."
echo "Base directory: $BASE_DIR"
echo ""

# Process DL folder (Deep Learning)
if [ -d "$INPUT_DIR/DL" ]; then
    echo "Processing Deep Learning videos..."
    for video in "$INPUT_DIR/DL"/*.mp4; do
        if [ -f "$video" ]; then
            transcribe_video "$video"
        fi
    done
fi

# Process RM folder (Research Methods)
if [ -d "$INPUT_DIR/RM" ]; then
    echo "Processing Research Methods videos..."
    for video in "$INPUT_DIR/RM"/*.mp4; do
        if [ -f "$video" ]; then
            transcribe_video "$video"
        fi
    done
fi

# Process BD folder (Big Data) if it has files
if [ -d "$INPUT_DIR/BD" ]; then
    echo "Processing Big Data videos..."
    for video in "$INPUT_DIR/BD"/*.mp4; do
        if [ -f "$video" ]; then
            transcribe_video "$video"
        fi
    done
fi

echo "=========================================="
echo "Transcription complete!"
echo "All transcripts saved to: $OUTPUT_DIR"
echo "=========================================="
