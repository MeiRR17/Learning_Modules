#!/usr/bin/env python3
"""
Script to remove consecutive repetitions from transcription files.
This helps clean up the whisper model's tendency to get stuck in loops.
"""

import os
import re
from pathlib import Path

def clean_srt_file(filepath):
    """Remove consecutive repetitions from SRT files."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    
    cleaned_lines = []
    prev_text = ""
    prev_timestamp = ""
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Check if it's a timestamp line
        if '-->' in line:
            current_timestamp = line
            # Get the text line(s) after timestamp
            i += 1
            text_lines = []
            while i < len(lines) and lines[i].strip() and '-->' not in lines[i]:
                text_lines.append(lines[i].strip())
                i += 1
            
            current_text = ' '.join(text_lines)
            
            # Skip if same text and timestamp as previous
            if current_text == prev_text and current_timestamp == prev_timestamp:
                continue
            
            # Skip if same text as previous (even with different timestamp)
            if current_text == prev_text:
                continue
            
            # Keep this entry
            cleaned_lines.append(f"{current_timestamp}\n")
            cleaned_lines.append(f"{current_text}\n\n")
            
            prev_text = current_text
            prev_timestamp = current_timestamp
        else:
            # It's a line number or other content
            if line.isdigit():
                cleaned_lines.append(f"{line}\n")
            else:
                cleaned_lines.append(f"{line}\n")
            i += 1
    
    # Write cleaned content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    print(f"Cleaned: {filepath}")

def clean_txt_file(filepath):
    """Remove consecutive repetitions from TXT files."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    
    cleaned_lines = []
    prev_line = ""
    
    for line in lines:
        current_line = line.strip()
        
        # Skip if same as previous
        if current_line == prev_line:
            continue
        
        # Skip if very similar to previous (edit distance < 3)
        if len(current_line) > 5 and len(prev_line) > 5:
            if current_line in prev_line or prev_line in current_line:
                continue
        
        cleaned_lines.append(line)
        prev_line = current_line
    
    # Write cleaned content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    print(f"Cleaned: {filepath}")

def clean_vtt_file(filepath):
    """Remove consecutive repetitions from VTT files."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    
    # Split by timestamp blocks
    blocks = re.split(r'(\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3})', content)
    
    cleaned_blocks = []
    prev_text = ""
    
    for i in range(1, len(blocks), 2):
        if i + 1 >= len(blocks):
            break
        
        timestamp = blocks[i]
        text = blocks[i + 1].strip()
        
        # Skip if same text as previous
        if text == prev_text:
            continue
        
        cleaned_blocks.append(timestamp)
        cleaned_blocks.append(text)
        prev_text = text
    
    # Reconstruct file
    cleaned_content = cleaned_blocks[0]  # Keep header
    for i in range(1, len(cleaned_blocks)):
        cleaned_content += cleaned_blocks[i]
        if i % 2 == 0:  # After text, add newline
            cleaned_content += "\n\n"
    
    # Write cleaned content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"Cleaned: {filepath}")

def main():
    output_dir = Path(os.environ.get("VIDEO_TO_TEXT_OUTPUT_DIR", str(Path(__file__).resolve().parent / "output")))
    
    # Process all files in output directory
    for course_dir in output_dir.iterdir():
        if course_dir.is_dir():
            print(f"\nProcessing {course_dir.name}...")
            for file in course_dir.iterdir():
                if file.is_file():
                    if file.suffix == '.srt':
                        clean_srt_file(file)
                    elif file.suffix == '.txt':
                        clean_txt_file(file)
                    elif file.suffix == '.vtt':
                        clean_vtt_file(file)
    
    print("\n✓ Cleaning complete!")

if __name__ == "__main__":
    main()
