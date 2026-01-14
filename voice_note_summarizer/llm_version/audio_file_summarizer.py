import os
import asyncio
import requests
import speech_recognition as sr
from agent_framework import ChatAgent
from agent_framework._types import ChatResponse, ChatMessage, Role, TextContent
from dotenv import load_dotenv
from pathlib import Path
import sys

load_dotenv()

# Puter API configuration
PUTER_API_URL = "https://api.puter.com/drivers/call"
PUTER_AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0IjoicyIsInYiOiIwLjAuMCIsInUiOiJzZ0NRbEhDVlFzaUoyRk1TSkMxVk9BPT0iLCJ1dSI6Im1aOXNsRFVVVHU2THFjN3orTGlPS1E9PSIsImlhdCI6MTc2ODQxNDY2MX0.aLvPKCILB45V93lPuJkJT7dz9qU1WuWzZYcjpXA-GbM"
PUTER_MODEL = "gpt-5-nano"

class PuterClient:
    def __init__(self, auth_token, model="gpt-5-nano"):
        self.auth_token = auth_token
        self.model = model

    @property
    def additional_properties(self):
        return {}

    async def get_response(self, messages, **kwargs):
        """
        Send messages to Puter's LLM API and return a ChatResponse.
        """
        # Convert messages to the format expected by Puter
        if isinstance(messages, str):
            message_content = messages
        elif isinstance(messages, list) and messages:
            # Take the last message if it's a list
            last_msg = messages[-1]
            if hasattr(last_msg, 'contents') and last_msg.contents:
                # ChatMessage has contents list
                first_content = last_msg.contents[0]
                if hasattr(first_content, 'text'):
                    message_content = first_content.text
                else:
                    message_content = str(first_content)
            elif hasattr(last_msg, 'content'):
                message_content = last_msg.content
            else:
                message_content = str(last_msg)
        else:
            message_content = "Hello"

        payload = {
            "interface": "puter-chat-completion",
            "driver": "ai-chat",
            "method": "complete",
            "args": {
                "messages": [{"content": message_content}],
                "model": self.model
            },
            "auth_token": self.auth_token
        }

        headers = {
            "Content-Type": "text/plain;actually=json",
            "user-agent": "puter-js/1.0",
            "origin": "https://puter.work",
            "referer": "https://puter.work/"
        }

        loop = asyncio.get_event_loop()
        response_text = await loop.run_in_executor(None, self._sync_request, payload, headers)

        # Create ChatResponse
        message = ChatMessage(role=Role.ASSISTANT, contents=[TextContent(text=response_text)])
        return ChatResponse(messages=[message])

    def _sync_request(self, payload, headers):
        try:
            response = requests.post(PUTER_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            if result.get("success"):
                return result["result"]["message"]["content"]
            else:
                return f"Error: {result.get('error', 'Unknown error')}"
        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"

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

async def main():
    print("AI Voice Note Summarizer - Audio File Version (LLM with MAF)")
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

        # Create the summarization agent
        chat_client = PuterClient(
            auth_token=PUTER_AUTH_TOKEN,
            model=PUTER_MODEL
        )

        agent = ChatAgent(
            chat_client=chat_client,
            instructions="""You are an expert at summarizing voice notes and meeting transcripts.
            Create clear, concise summaries that capture the key points, decisions, and action items.
            Structure your summaries with:
            - Main topics discussed
            - Key decisions made
            - Action items with owners if mentioned
            - Important dates or deadlines
            Keep summaries brief but comprehensive.""",
            name="Voice Note Summarizer"
        )

        # Transcribe
        print("Transcribing...")
        transcription = transcribe_audio(audio)
        print(f"\nTranscription:\n{transcription}\n")

        if transcription in ["Could not understand audio", ""]:
            print("No valid transcription to summarize.")
            return

        # Summarize using the agent
        print("Summarizing with AI...")
        prompt = f"Please summarize the following audio transcription:\n\n{transcription}"
        result = await agent.run(prompt)
        print(f"\nAI Summary:\n{result.text}")

        # Save results
        output_file = Path(file_path).stem + "_summary.txt"
        with open(output_file, 'w') as f:
            f.write(f"Original Transcription:\n{transcription}\n\n")
            f.write(f"AI Summary:\n{result.text}\n")
        print(f"\nResults saved to: {output_file}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
