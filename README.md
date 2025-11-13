# Whisper Subtitle Generator

A command line tool that generates SRT subtitles from audio or video
files using the OpenAI Whisper model.

The script automatically checks for ffmpeg, handles CPU or GPU
selection, supports multiple Whisper models, and offers configurable
options such as language, output path, and transcription or translation
mode.

This tool is ideal for transcribing interviews, videos, podcasts,
lectures, voice notes, and any other audio content.

## Features

- Automatic SRT subtitle generation
- Accepts audio and video files, including MP4
- Automatically extracts the audio track from video using ffmpeg
- Uses OpenAI Whisper for accurate speech recognition
- Supports multiple models (tiny, base, small, medium, large)
- CPU and GPU compatible
- Automatic fallback if GPU is not available
- Customizable language
- Supports both transcription and translation
- Clean, human readable error messages
- Optional verbose mode for debugging
- Reminds users to check `--help` when no arguments are provided

## Video Support

The script fully supports video files such as:

- .mp4
- .mkv
- .mov
- .avi
- and any other format supported by ffmpeg

When you pass a video file (for example `video.mp4`), ffmpeg
automatically extracts the audio track. The script then generates an
SRT file using the same base name:

Input:

```
python3 subtitles.py video.mp4
```

Output:

```
video.srt
```

No manual conversion to WAV is required.

## Requirements

### 1. Python 3.8 or later

### 2. Required Python packages

```
pip install openai-whisper torch
```

### 3. ffmpeg

On Ubuntu or Debian:

```
sudo apt update
sudo apt install ffmpeg
```

## Installation

```
git clone https://github.com/gerlandotermini/subtitle-generator.git
cd subtitle-generator
```

## Usage

Basic usage with audio:

```
python3 subtitles.py input.wav
```

Basic usage with video:

```
python3 subtitles.py input.mp4
```

Full help:

```
python3 subtitles.py --help
```

## License

MIT License
