@echo off
REM Kokoro TTS Batch Converter
REM Processes all files in text_input folder

echo ========================================
echo    Kokoro TTS Batch Converter
echo ========================================
echo.

REM Check if text_input folder exists
if not exist "text_input" (
    echo Error: text_input folder not found!
    echo Please create the text_input folder and put your text files in it.
    pause
    exit /b 1
)

REM Create necessary directories
if not exist "audio_output" mkdir audio_output
if not exist "completed" mkdir completed

REM Read config file
set VOICE=af_bella
set SPEED=1.0

if exist "config.txt" (
    for /f "tokens=1,2 delims==" %%a in (config.txt) do (
        if "%%a"=="VOICE" set VOICE=%%b
        if "%%a"=="SPEED" set SPEED=%%b
    )
)

echo Using voice: %VOICE%
echo Using speed: %SPEED%x
echo.

REM Enable delayed expansion for variables in loops
setlocal enabledelayedexpansion

REM Process all .txt files
set FILE_COUNT=0
for %%F in (text_input\*.txt) do (
    set /a FILE_COUNT+=1
    echo Processing file !FILE_COUNT!: %%~nxF
    echo Start time: %date% %time%
    echo.
    
    REM Convert using Python script
    python text_to_audio_batch.py "%%F" %VOICE% %SPEED%
    
    if !ERRORLEVEL! EQU 0 (
        echo.
        echo ========================================
        echo    File Complete: %%~nxF
        echo    End time: %date% %time%
        echo ========================================
        echo.
        
        REM Move completed file
        move "%%F" "completed\%%~nxF"
    ) else (
        echo.
        echo ========================================
        echo    FAILED: %%~nxF
        echo ========================================
        echo.
    )
)

if %FILE_COUNT% EQU 0 (
    echo No .txt files found in text_input folder!
    echo Please put some text files in the text_input folder.
) else (
    echo.
    echo ========================================
    echo    Batch Processing Complete!
    echo ========================================
    echo Processed %FILE_COUNT% files
    echo Completed files moved to: completed\
    echo Audio files saved to: audio_output\
)

echo.
pause