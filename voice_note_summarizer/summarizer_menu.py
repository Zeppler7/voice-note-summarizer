#!/usr/bin/env python
"""
AI Voice Note Summarizer - Main Menu
Provides three options:
1. Record live audio from microphone
2. Process an audio file
3. Test mode with sample transcription
"""

import sys
import subprocess
from pathlib import Path

def show_menu():
    """Display the main menu"""
    print("\n" + "=" * 70)
    print("AI VOICE NOTE SUMMARIZER - MAIN MENU")
    print("=" * 70)
    print("\nChoose a summarizer version:")
    print("\n1. Non-LLM Version (Traditional NLP)")
    print("   - Extractive summarization using word frequency analysis")
    print("   - Faster and no internet required for summarization")
    print()
    print("2. LLM Version (AI-Powered with Puter)")
    print("   - Intelligent summarization using Puter's free LLM")
    print("   - Structured output with topics, decisions, and action items")
    print()
    print("3. Exit")
    print("\n" + "=" * 70)

def choose_mode():
    """Choose how to process audio"""
    print("\nChoose input mode:")
    print("\n1. Live Recording (10 seconds from microphone)")
    print("2. Audio File (process existing WAV, MP3, FLAC, OGG, M4A)")
    print("3. Test Mode (use sample transcription)")
    print()
    choice = input("Enter choice (1-3): ").strip()
    return choice

def get_script_path(version, mode):
    """Get the path to the appropriate script"""
    base_path = Path(__file__).parent / "voice_note_summarizer"
    
    if version == "1":
        script_dir = base_path / "non_llm_version"
    elif version == "2":
        script_dir = base_path / "llm_version"
    else:
        return None
    
    if mode == "1":
        return script_dir / "voice_summarizer.py"
    elif mode == "2":
        return script_dir / "audio_file_summarizer.py"
    elif mode == "3":
        return script_dir / "voice_summarizer.py"
    
    return None

def run_non_llm(mode):
    """Run the non-LLM version"""
    base_path = Path(__file__).parent / "non_llm_version"
    
    if mode == "1":
        script = base_path / "voice_summarizer.py"
        if not script.exists():
            print(f"Error: Script not found at {script}")
            return
        print(f"\nRunning: Non-LLM Voice Summarizer")
        print("-" * 70)
        subprocess.run([sys.executable, str(script)])
        
    elif mode == "2":
        script = base_path / "audio_file_summarizer.py"
        if not script.exists():
            print(f"Error: Script not found at {script}")
            return
        print(f"\nRunning: Non-LLM Audio File Summarizer")
        print("-" * 70)
        subprocess.run([sys.executable, str(script)])
        
    elif mode == "3":
        script = base_path / "voice_summarizer.py"
        if not script.exists():
            print(f"Error: Script not found at {script}")
            return
        print(f"\nRunning: Non-LLM Voice Summarizer (Test Mode)")
        print("-" * 70)
        subprocess.run([sys.executable, str(script), "--test"])

def run_llm(mode):
    """Run the LLM version"""
    base_path = Path(__file__).parent / "llm_version"
    
    if mode == "1":
        script = base_path / "voice_summarizer.py"
        if not script.exists():
            print(f"Error: Script not found at {script}")
            return
        print(f"\nRunning: LLM Voice Summarizer (with Puter AI)")
        print("-" * 70)
        subprocess.run([sys.executable, str(script)])
        
    elif mode == "2":
        script = base_path / "audio_file_summarizer.py"
        if not script.exists():
            print(f"Error: Script not found at {script}")
            return
        print(f"\nRunning: LLM Audio File Summarizer (with Puter AI)")
        print("-" * 70)
        subprocess.run([sys.executable, str(script)])
        
    elif mode == "3":
        script = base_path / "voice_summarizer.py"
        if not script.exists():
            print(f"Error: Script not found at {script}")
            return
        print(f"\nRunning: LLM Voice Summarizer (Test Mode)")
        print("-" * 70)
        subprocess.run([sys.executable, str(script), "--test"])

def main():
    while True:
        show_menu()
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            # Non-LLM Version
            mode = choose_mode()
            run_non_llm(mode)
            
        elif choice == "2":
            # LLM Version
            mode = choose_mode()
            run_llm(mode)
            
        elif choice == "3":
            # Exit
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
