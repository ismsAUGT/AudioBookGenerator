#!/usr/bin/env python3
"""
Kokoro TTS Batch Converter
Processes individual files with progress tracking
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

def convert_text_to_audio(input_file, voice="af_bella", speed=1.0):
    """
    Convert a text file to audio using Kokoro TTS
    
    Args:
        input_file (str): Path to the input text file
        voice (str): Voice to use (default: af_bella)
        speed (float): Speech speed (default: 1.0)
    """
    
    # Validate input file
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: Input file '{input_file}' not found!")
        return False
    
    # Get output filename (same as input but .wav)
    output_name = input_path.stem
    output_file = Path("audio_output") / f"{output_name}.wav"
    
    # Create output directory
    Path("audio_output").mkdir(exist_ok=True)
    
    print(f"Converting '{input_path.name}' to audio...")
    print(f"Voice: {voice}")
    print(f"Speed: {speed}x")
    print(f"Output: {output_file}")
    print(f"File size: {input_path.stat().st_size:,} bytes")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        # Build the command
        cmd = [
            "python", "-m", "kokoro_tts_cli.streamer",
            "--voice", voice,
            "--speed", str(speed),
            "--save", str(output_file),
            "--no-play",
            "--batch",
            "--verbose"
        ]
        
        # Read input file and pipe to command
        with open(input_file, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Ensure file is closed before running subprocess
        process = subprocess.run(
            cmd,
            input=file_content,
            text=True,
            capture_output=True,
            cwd=Path.cwd()
        )
        
        # Small delay to ensure file handles are released
        time.sleep(0.1)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if process.returncode == 0:
            print(f"Success! Audio saved to: {output_file}")
            print(f"Processing time: {duration:.1f} seconds ({duration/60:.1f} minutes)")
            return True
        else:
            print(f"Error during conversion:")
            if process.stderr:
                print(process.stderr)
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main function - called by batch script"""
    
    if len(sys.argv) < 2:
        print("This script is called by convert.bat")
        print("Please run convert.bat instead.")
        return False
    
    input_file = sys.argv[1]
    voice = sys.argv[2] if len(sys.argv) > 2 else "af_bella"
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    
    return convert_text_to_audio(input_file, voice, speed)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
