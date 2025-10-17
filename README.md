# Kokoro TTS Auto-Converter

A simple, automated text-to-speech converter using Kokoro TTS. Just drop a text file and convert!

## 🚀 Quick Start

1. **Put your text file** in the `text_input` folder
2. **Run** `convert.bat`
3. **Get your audio** from the `audio_output` folder

That's it! The system automatically:
- Finds the text file in `text_input`
- Uses your preferred voice from `config.txt`
- Saves the audio with the same filename (but .wav extension)

## ⚙️ Configuration

Edit `config.txt` to change your settings:

```
VOICE=af_bella    # Change this to your preferred voice
SPEED=1.0         # Adjust speech speed (0.5-2.0)
```

### Available Voices

**American English:**
- `af_bella` - Bella (female) - *Recommended*
- `af_sarah` - Sarah (female)
- `af_nicole` - Nicole (female)
- `am_adam` - Adam (male)
- `am_michael` - Michael (male)

**British English:**
- `bf_emma` - Emma (female)
- `bf_isabella` - Isabella (female)
- `bm_george` - George (male)
- `bm_lewis` - Lewis (male)

## 📁 Folder Structure

```
KokoroTTS/
├── text_input/          # Put your .txt files here
├── audio_output/        # Audio files are saved here
├── config.txt           # Edit this to change voice/speed
├── convert.bat          # Run this to convert
└── README.md           # This file
```

## 🔄 Workflow

1. **Drop** your text file in `text_input/`
2. **Run** `convert.bat`
3. **Find** your audio in `audio_output/`
4. **Replace** the text file and run again for new conversions

## 💡 Tips

- Only put **one text file** at a time in `text_input/`
- The output audio will have the **same name** as your input file
- Supported formats: `.txt` files with UTF-8 encoding
- For best results, keep text files under 10,000 characters

## 🎵 Example

1. Put `my_story.txt` in `text_input/`
2. Run `convert.bat`
3. Get `my_story.wav` in `audio_output/`

Enjoy your high-quality text-to-speech conversions! 🎉

