# AI Voice Note Summarizer

This project contains multiple implementations of an AI Voice Note Summarizer with three input modes:

1. **Live Recording** - Records audio directly from your microphone
2. **Audio File Processing** - Processes existing audio files (WAV, MP3, FLAC, OGG, M4A)
3. **Test Mode** - Tests with sample transcription (no microphone required)

## Summarizer Versions

1. **Non-LLM Version** (`non_llm_version/`): Uses traditional NLP techniques with NLTK for extractive summarization
2. **LLM Version** (`llm_version/`): Uses Microsoft Agentic Framework (MAF) with Puter.com's free LLM API for intelligent summarization

## Features

- **Audio Recording**: Records audio from microphone for a specified duration
- **Audio File Support**: Process existing audio files (new feature!)
- **Speech-to-Text**: Transcribes audio using Google Speech Recognition API
- **Summarization**:
  - Non-LLM: Extractive summarization based on word frequency scoring
  - LLM: AI-powered summarization with structured output including topics, decisions, and action items

## Prerequisites

- Python 3.12+
- Microphone for audio recording (optional - can use audio files instead)
- Internet connection for speech recognition and LLM API calls

## Setup

### Installation

```bash
# Install dependencies for non-LLM version
cd non_llm_version
pip install -r requirements.txt

# Install dependencies for LLM version
cd ../llm_version
pip install -r requirements.txt
```

### Quick Start - Menu Interface

Use the interactive menu to choose summarizer and input mode:

```bash
python summarizer_menu.py
```

This provides a user-friendly menu to:
- Choose between Non-LLM or LLM version
- Select input mode (Live Recording, Audio File, or Test Mode)

### Direct Usage

#### Non-LLM Version

```bash
cd non_llm_version

# Live recording (10 seconds)
python voice_summarizer.py

# Process audio file
python audio_file_summarizer.py
# Then enter the path to your audio file when prompted

# Test mode
python voice_summarizer.py --test

# Use specific microphone
python voice_summarizer.py --mic 1
```

#### LLM Version

```bash
cd llm_version

# Live recording (10 seconds)
python voice_summarizer.py

# Process audio file
python audio_file_summarizer.py
# Then enter the path to your audio file when prompted

# Test mode
python voice_summarizer.py --test

# Use specific microphone
python voice_summarizer.py --mic 1
```

## Usage

### Command Line Options

**Live Recording & Audio File modes:**
- `--test`: Run in test mode with sample transcription (no microphone required)
- `--mic <number>`: Specify microphone device index (see available microphones below)

### Examples

**Test Mode (recommended for development):**
```bash
# Non-LLM version
cd non_llm_version
python voice_summarizer.py --test

# LLM version
cd llm_version
python voice_summarizer.py --test
```

**Process Audio Files:**
```bash
# Non-LLM version
cd non_llm_version
python audio_file_summarizer.py
# Enter path: d:\Python Projects\harvard.wav

# LLM version
cd llm_version
python audio_file_summarizer.py
# Enter path: d:\Python Projects\harvard.wav
```

**With Microphone:**
```bash
# Non-LLM version
cd non_llm_version
python voice_summarizer.py

# LLM version
cd llm_version
python voice_summarizer.py

# Using specific microphone
python voice_summarizer.py --mic 1
```

### Available Microphones

Run this command to see available microphones on your system:
```python
import speech_recognition as sr
mics = sr.Microphone.list_microphone_names()
for i, name in enumerate(mics):
    print(f"{i}: {name}")
```

## Dependencies

### Non-LLM Version
- `speech_recognition`: For audio recording and Google Speech API
- `nltk`: For natural language processing and text analysis
- `pyaudio`: For microphone access

### LLM Version
- `agent_framework`: Microsoft Agentic Framework for AI agent orchestration
- `requests`: For HTTP API calls to Puter
- `python-dotenv`: For environment variable management
- `speech_recognition`: For audio recording and Google Speech API
- `pyaudio`: For microphone access

## API Keys

- **Google Speech Recognition**: No API key required (uses free tier)
- **Puter LLM**: Uses free API with included auth token (no signup required)

## Output Format

### Non-LLM Version
- Simple extractive summary selecting key sentences
- Text file saved with transcription and summary

### LLM Version
- Structured summary with:
  - Main topics discussed
  - Key decisions made
  - Action items with owners (if mentioned)
  - Important dates or deadlines
- Text file saved with transcription and AI summary

## Supported Audio Formats

- WAV (recommended, fully supported)
- MP3 (requires ffmpeg)
- FLAC (requires ffmpeg)
- OGG (requires ffmpeg)
- M4A (requires ffmpeg)

## Limitations

- Live recording duration is fixed at 10 seconds
- Requires internet connection for transcription and LLM calls
- Google Speech API has usage limits
- Puter API may have rate limits
- Audio files with heavy background noise (like jackhammer.wav) may not transcribe well

## Project Structure

```
voice_note_summarizer/
├── README.md                          # This file
├── summarizer_menu.py                 # Interactive menu interface
├── non_llm_version/
│   ├── voice_summarizer.py            # Live recording & test mode
│   ├── audio_file_summarizer.py       # Audio file processing
│   └── requirements.txt               # Non-LLM dependencies
└── llm_version/
    ├── voice_summarizer.py            # Live recording & test mode with MAF
    ├── audio_file_summarizer.py       # Audio file processing with MAF
    ├── requirements.txt               # LLM dependencies
    └── .env                           # Puter API token
```

## Future Enhancements

- Support for more audio formats
- Adjustable recording duration
- Multiple language support
- Batch processing of multiple audio files
- Audio preprocessing (noise reduction)
- Web interface
- Cloud storage integration