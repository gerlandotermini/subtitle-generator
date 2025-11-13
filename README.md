# Whisper Subtitle Generator

A command line tool that generates SRT subtitles from audio or video
files using the OpenAI Whisper model.\
The script automatically checks for ffmpeg, handles CPU or GPU
selection, supports multiple Whisper models, and offers configurable
options such as language, output path, and transcription or translation
mode.

This tool is ideal for transcribing interviews, videos, podcasts,
lectures, voice notes, and any other audio content.

## Features

-   Automatic SRT subtitle generation
-   Uses OpenAI Whisper for accurate speech recognition
-   Supports multiple models (tiny, base, small, medium, large)
-   Works with audio and video files
-   CPU and GPU compatible
-   Automatic fallback if GPU is not available
-   Customizable language
-   Supports both transcription and translation
-   Clean, human readable error messages
-   Optional verbose mode for debugging
-   Reminds users to check `--help` when no arguments are provided

## Requirements

### 1. Python 3.8 or later

### 2. Required Python packages

    pip install openai-whisper torch

### 3. ffmpeg

On Ubuntu or Debian:

    sudo apt update
    sudo apt install ffmpeg

## Installation

    git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    cd YOUR_REPO_NAME

## Usage

Basic usage:

    python3 genera_sottotitoli.py input.wav

Full help:

    python3 genera_sottotitoli.py --help

## License

MIT License
