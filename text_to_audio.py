#!/usr/bin/env python3
"""
Kokoro TTS Text-to-Audio Converter
Simple script to convert text files to high-quality audio
"""

import os
import sys
import subprocess
from pathlib import Path

def convert_text_to_audio(input_file, voice="af_bella", output_name=None, speed=1.0):
    """
    Convert a text file to audio using Kokoro TTS
    
    Args:
        input_file (str): Path to the input text file
        voice (str): Voice to use (default: af_bella)
        output_name (str): Output filename (default: same as input)
        speed (float): Speech speed (default: 1.0)
    """
    
    # Validate input file
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: Input file '{input_file}' not found!")
        return False
    
    # Set output name
    if output_name is None:
        output_name = input_path.stem
    
    # Create output directory
    output_dir = Path("audio_output")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"{output_name}.wav"
    
    print(f"Converting '{input_file}' to audio...")
    print(f"Voice: {voice}")
    print(f"Speed: {speed}x")
    print(f"Output: {output_file}")
    print("-" * 50)
    
    try:
        # Build the command
        cmd = [
            "python", "-m", "kokoro_tts_cli.streamer",
            "--voice", voice,
            "--speed", str(speed),
            "--save", str(output_file),
            "--no-play",
            "--batch"
        ]
        
        # Read input file and pipe to command
        with open(input_file, 'r', encoding='utf-8') as f:
            process = subprocess.run(
                cmd,
                input=f.read(),
                text=True,
                capture_output=True,
                cwd=Path.cwd()
            )
        
        if process.returncode == 0:
            print(f"\n✅ Success! Audio saved to: {output_file}")
            return True
        else:
            print(f"\n❌ Error during conversion:")
            print(process.stderr)
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    """Main function with command line interface"""
    
    if len(sys.argv) < 2:
        print("Kokoro TTS Text-to-Audio Converter")
        print("=" * 40)
        print("Usage:")
        print("  python text_to_audio.py <input_file> [voice] [output_name] [speed]")
        print()
        print("Examples:")
        print("  python text_to_audio.py story.txt")
        print("  python text_to_audio.py story.txt af_bella")
        print("  python text_to_audio.py story.txt bf_emma my_story")
        print("  python text_to_audio.py story.txt af_bella my_story 1.2")
        print()
        print("Available voices:")
        print("  American: af_bella, af_sarah, am_adam, am_michael")
        print("  British:  bf_emma, bf_isabella, bm_george, bm_lewis")
        return
    
    input_file = sys.argv[1]
    voice = sys.argv[2] if len(sys.argv) > 2 else "af_bella"
    output_name = sys.argv[3] if len(sys.argv) > 3 else None
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    
    success = convert_text_to_audio(input_file, voice, output_name, speed)
    
    if success:
        print("\n🎵 Ready to listen! Check the audio_output folder.")
    else:
        print("\n💡 Tip: Make sure your text file is in UTF-8 encoding.")

if __name__ == "__main__":
    main()

