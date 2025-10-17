@echo off
REM Kokoro TTS Text-to-Audio Converter
REM Usage: convert_to_audio.bat input_file.txt [voice] [output_name]

set INPUT_FILE=%1
set VOICE=%2
set OUTPUT_NAME=%3

REM Set defaults if not provided
if "%VOICE%"=="" set VOICE=af_bella
if "%OUTPUT_NAME%"=="" (
    for %%F in ("%INPUT_FILE%") do set OUTPUT_NAME=%%~nF
)

REM Create output directory if it doesn't exist
if not exist "audio_output" mkdir audio_output

REM Convert text to audio
echo Converting %INPUT_FILE% to audio using voice %VOICE%...
echo Output will be saved as: audio_output\%OUTPUT_NAME%.wav

type "%INPUT_FILE%" | python -m kokoro_tts_cli.streamer --voice %VOICE% --save "audio_output\%OUTPUT_NAME%.wav" --no-play --batch

echo.
echo Conversion complete! Check audio_output\%OUTPUT_NAME%.wav
pause

