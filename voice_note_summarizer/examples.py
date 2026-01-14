#!/usr/bin/env python
"""
AI Voice Note Summarizer - Usage Examples

This script shows practical examples of how to use the audio file processing feature.
"""

import subprocess
import sys
from pathlib import Path

def example_1():
    """Example 1: Process audio file with Non-LLM version"""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Process Audio File with Non-LLM Version")
    print("=" * 70)
    print("\nThis example shows how to process an audio file using")
    print("traditional NLP-based summarization.")
    print("\nCommand:")
    print("  python audio_file_summarizer.py 'path/to/audio.wav'")
    print("\nOutput:")
    print("  - Transcription (speech to text)")
    print("  - Summary (extractive summarization)")
    print("  - Results saved to {filename}_summary.txt")
    
    base_path = Path(__file__).parent / "voice_note_summarizer" / "non_llm_version"
    script = base_path / "audio_file_summarizer.py"
    
    print("\n" + "-" * 70)
    print("Running example...")
    print("-" * 70)
    
    subprocess.run([sys.executable, str(script), "d:\\Python Projects\\harvard.wav"])

def example_2():
    """Example 2: Process audio file with LLM version"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Process Audio File with LLM Version (AI-Powered)")
    print("=" * 70)
    print("\nThis example shows how to process an audio file using")
    print("intelligent AI-powered summarization with Puter LLM.")
    print("\nCommand:")
    print("  python audio_file_summarizer.py 'path/to/audio.wav'")
    print("\nOutput:")
    print("  - Transcription (speech to text)")
    print("  - AI Summary (with topics, decisions, action items)")
    print("  - Results saved to {filename}_summary.txt")
    
    base_path = Path(__file__).parent / "voice_note_summarizer" / "llm_version"
    script = base_path / "audio_file_summarizer.py"
    
    print("\n" + "-" * 70)
    print("Running example...")
    print("-" * 70)
    
    subprocess.run([sys.executable, str(script), "d:\\Python Projects\\harvard.wav"])

def example_3():
    """Example 3: Compare both versions"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Compare Non-LLM vs LLM Summaries")
    print("=" * 70)
    print("\nProcess the same audio file with both versions to compare")
    print("traditional NLP vs AI-powered summarization.")
    print("\nNon-LLM Version (Fast, no internet for summarization)")
    print("LLM Version (AI-powered, requires internet)")
    
    print("\n" + "-" * 70)
    print("Running Non-LLM version...")
    print("-" * 70)
    
    base_path = Path(__file__).parent / "voice_note_summarizer" / "non_llm_version"
    script = base_path / "audio_file_summarizer.py"
    subprocess.run([sys.executable, str(script), "d:\\Python Projects\\harvard.wav"])
    
    print("\n" + "-" * 70)
    print("Running LLM version...")
    print("-" * 70)
    
    base_path = Path(__file__).parent / "voice_note_summarizer" / "llm_version"
    script = base_path / "audio_file_summarizer.py"
    subprocess.run([sys.executable, str(script), "d:\\Python Projects\\harvard.wav"])

def example_4():
    """Example 4: Using the interactive menu"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Interactive Menu")
    print("=" * 70)
    print("\nUse the interactive menu to choose options:")
    print("\n1. Select version (Non-LLM or LLM)")
    print("2. Select input mode:")
    print("   - Live Recording (microphone)")
    print("   - Audio File (upload/select file)")
    print("   - Test Mode (sample transcription)")
    print("\nThe menu guides you through each step.")
    
    base_path = Path(__file__).parent / "voice_note_summarizer"
    script = base_path / "summarizer_menu.py"
    
    print("\n" + "-" * 70)
    print("Starting interactive menu...")
    print("-" * 70)
    
    subprocess.run([sys.executable, str(script)])

def main():
    print("\n" + "=" * 70)
    print("AI VOICE NOTE SUMMARIZER - USAGE EXAMPLES")
    print("=" * 70)
    print("\nAvailable examples:")
    print("\n1. Non-LLM Audio File Processing")
    print("   Traditional NLP-based summarization")
    print("\n2. LLM Audio File Processing")
    print("   AI-powered summarization")
    print("\n3. Compare Both Versions")
    print("   See difference between approaches")
    print("\n4. Interactive Menu")
    print("   Choose version and input mode")
    print("\n5. Exit")
    
    while True:
        choice = input("\n\nEnter example number (1-5): ").strip()
        
        if choice == "1":
            example_1()
        elif choice == "2":
            example_2()
        elif choice == "3":
            example_3()
        elif choice == "4":
            example_4()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")
        
        input("\n\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExamples interrupted. Goodbye!")
        sys.exit(0)
