#!/usr/bin/env python
"""
AI Voice Note Summarizer - Quick Start Guide

This script provides an interactive demo of all three input modes
for both the Non-LLM and LLM versions of the voice note summarizer.
"""

import subprocess
import sys
from pathlib import Path

def run_demo(script_path, args=None, description=""):
    """Run a demo script and display the description"""
    print("\n" + "=" * 70)
    print(f"Demo: {description}")
    print("=" * 70)
    
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nDemo interrupted.")
    except Exception as e:
        print(f"Error running demo: {e}")

def main():
    print("\n" + "=" * 70)
    print("AI VOICE NOTE SUMMARIZER - QUICK START DEMO")
    print("=" * 70)
    print("\nThis demo will show you all the available features.")
    print("\nAvailable demos:")
    print("1. Non-LLM - Test Mode (recommended first)")
    print("2. Non-LLM - Audio File (harvard.wav)")
    print("3. LLM - Test Mode")
    print("4. LLM - Audio File (harvard.wav)")
    print("5. Run Interactive Menu")
    print("6. Exit")
    
    base_path = Path(__file__).parent / "voice_note_summarizer"
    
    while True:
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            script = base_path / "non_llm_version" / "voice_summarizer.py"
            run_demo(script, ["--test"], 
                    "Non-LLM Version - Test Mode")
            
        elif choice == "2":
            script = base_path / "non_llm_version" / "audio_file_summarizer.py"
            run_demo(script,
                    ["d:\\Python Projects\\harvard.wav"],
                    "Non-LLM Version - Audio File Processing")
            
        elif choice == "3":
            script = base_path / "llm_version" / "voice_summarizer.py"
            run_demo(script, ["--test"],
                    "LLM Version - Test Mode")
            
        elif choice == "4":
            script = base_path / "llm_version" / "audio_file_summarizer.py"
            run_demo(script,
                    ["d:\\Python Projects\\harvard.wav"],
                    "LLM Version - Audio File Processing")
            
        elif choice == "5":
            menu_script = base_path / "summarizer_menu.py"
            try:
                subprocess.run([sys.executable, str(menu_script)])
            except KeyboardInterrupt:
                print("\nMenu interrupted.")
            
        elif choice == "6":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")
        sys.exit(0)
