#!/usr/bin/env python
import speech_recognition as sr
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string
import os
from pathlib import Path
import sys

# Download required NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

def load_audio_file(file_path):
    """
    Load an audio file and return the audio data.
    Supports: WAV, MP3, FLAC, OGG, M4A
    """
    recognizer = sr.Recognizer()
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    # Determine file type
    suffix = file_path.suffix.lower()
    
    try:
        if suffix == '.wav':
            with sr.AudioFile(str(file_path)) as source:
                audio = recognizer.record(source)
        elif suffix in ['.mp3', '.flac', '.ogg', '.m4a']:
            # These formats require ffmpeg to be installed
            with sr.AudioFile(str(file_path)) as source:
                audio = recognizer.record(source)
        else:
            raise ValueError(f"Unsupported audio format: {suffix}")

        return audio
    except Exception as e:
        raise RuntimeError(f"Error loading audio file: {e}")

def transcribe_audio(audio):
    """
    Transcribe audio to text using Google Speech Recognition.
    """
    recognizer = sr.Recognizer()

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

def extractive_summarize(text, num_sentences=3):
    """
    Create an extractive summary by selecting the most important sentences.
    """
    if not text or text in ["Could not understand audio", ""]:
        return "No valid text to summarize."

    # Tokenize into sentences
    sentences = sent_tokenize(text)

    if len(sentences) <= num_sentences:
        return text

    # Preprocess text
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())

    # Remove punctuation and stop words
    words = [word for word in words if word not in stop_words and word not in string.punctuation]

    # Calculate word frequencies
    word_freq = Counter(words)

    # Score sentences based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        sentence_words = word_tokenize(sentence.lower())
        sentence_words = [word for word in sentence_words if word not in string.punctuation]
        score = sum(word_freq.get(word, 0) for word in sentence_words)
        sentence_scores[sentence] = score

    # Select top sentences
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    summary = ' '.join([sentence for sentence, score in sorted(top_sentences, key=lambda x: sentences.index(x[0]))])

    return summary

def main():
    print("AI Voice Note Summarizer - Audio File Version (Non-LLM)")
    print("=" * 60)

    # Get audio file path from user or command line
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter the path to your audio file: ").strip()

    if not file_path:
        print("No file path provided.")
        return

    try:
        # Load audio file
        print(f"Loading audio file: {file_path}")
        audio = load_audio_file(file_path)

        # Transcribe
        print("Transcribing...")
        transcription = transcribe_audio(audio)
        print(f"\nTranscription:\n{transcription}\n")

        if transcription in ["Could not understand audio", ""]:
            print("No valid transcription to summarize.")
            return

        # Summarize
        print("Summarizing...")
        summary = extractive_summarize(transcription)
        print(f"\nSummary:\n{summary}")

        # Save results
        output_file = Path(file_path).stem + "_summary.txt"
        with open(output_file, 'w') as f:
            f.write(f"Original Transcription:\n{transcription}\n\n")
            f.write(f"Summary:\n{summary}\n")
        print(f"\nResults saved to: {output_file}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
