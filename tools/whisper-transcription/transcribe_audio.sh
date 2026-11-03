#!/bin/bash

# Script to transcribe all WAV audio files in Input/audio using whisper.cpp
# Uses the large-v3-turbo model with Hebrew language support

# Set paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="${BASE_DIR:-$SCRIPT_DIR}"
INPUT_DIR="$BASE_DIR/Input/audio"
OUTPUT_DIR="$BASE_DIR/output/audio"
WHISPER_DIR="$BASE_DIR/whisper.cpp"
MODEL_PATH="$WHISPER_DIR/models/ggml-large-v3-turbo.bin"
WHISPER_CLI="$WHISPER_DIR/build/bin/whisper-cli"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check model and binary exist
if [ ! -f "$MODEL_PATH" ]; then
    echo "Error: Model not found: $MODEL_PATH"
    exit 1
fi

if [ ! -f "$WHISPER_CLI" ]; then
    echo "Error: whisper-cli not found: $WHISPER_CLI"
    exit 1
fi

# Count total files
total=0
for audio in "$INPUT_DIR"/*.wav; do
    [ -f "$audio" ] && ((total++))
done

echo "=========================================="
echo "Starting transcription of all WAV files"
echo "Model: large-v3-turbo"
echo "Total files: $total"
echo "Output directory: $OUTPUT_DIR"
echo "Started at: $(date)"
echo "=========================================="

current=0
for audio in "$INPUT_DIR"/*.wav; do
    [ -f "$audio" ] || continue
    
    audio_name=$(basename "$audio")
    base_name="${audio_name%.*}"
    
    ((current++))
    
    # Skip if already transcribed
    if [ -f "$OUTPUT_DIR/$base_name.txt" ] && [ -f "$OUTPUT_DIR/$base_name.srt" ] && [ -f "$OUTPUT_DIR/$base_name.vtt" ]; then
        echo "[$current/$total] Skipping (already transcribed): $audio_name"
        continue
    fi
    
    echo ""
    echo "=========================================="
    echo "[$current/$total] Transcribing: $audio_name"
    echo "Started: $(date)"
    echo "=========================================="
    
    DYLD_LIBRARY_PATH="$WHISPER_DIR/build/src:$WHISPER_DIR/build/ggml/src:$WHISPER_DIR/build/ggml/src/ggml-metal:$WHISPER_DIR/build/ggml/src/ggml-blas" "$WHISPER_CLI" \
        -l he \
        -m "$MODEL_PATH" \
        -f "$audio" \
        -of "$OUTPUT_DIR/$base_name" \
        -otxt \
        -osrt \
        -ovtt \
        -t 8 \
        --processors 1 \
        --split-on-word \
        --max-len 30 \
        --temperature 0.0
    
    whisper_status=$?
    
    if [ $whisper_status -eq 0 ]; then
        echo "Finished: $(date)"
        echo "Output: $OUTPUT_DIR/$base_name.{txt,srt,vtt}"
    else
        echo "Error transcribing $audio_name (exit code: $whisper_status)"
    fi
done

echo ""
echo "=========================================="
echo "Transcription complete!"
echo "Finished at: $(date)"
echo "All transcripts saved to: $OUTPUT_DIR"
echo "=========================================="
