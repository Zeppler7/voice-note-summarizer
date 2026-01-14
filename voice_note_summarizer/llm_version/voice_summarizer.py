import os
import asyncio
import requests
import speech_recognition as sr
from agent_framework import ChatAgent
from agent_framework._types import ChatResponse, ChatMessage, Role, TextContent
from dotenv import load_dotenv

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

def record_audio(duration=10, test_mode=False, mic_index=None):
    """
    Record audio from microphone for specified duration.
    In test mode, returns None to simulate no audio.
    """
    if test_mode:
        print(f"Test mode: Simulating {duration} seconds of recording...")
        return None

    recognizer = sr.Recognizer()

    try:
        # Try to use specified microphone or default
        if mic_index is not None:
            print(f"Using microphone {mic_index}")
            with sr.Microphone(device_index=mic_index) as source:
                print(f"Recording for {duration} seconds... Speak now!")
                print("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = recognizer.listen(source, timeout=duration)
        else:
            with sr.Microphone() as source:
                print(f"Recording for {duration} seconds... Speak now!")
                print("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = recognizer.listen(source, timeout=duration)

        print("Recording completed.")
        return audio
    except sr.WaitTimeoutError:
        print("No audio detected within timeout period.")
        return None
    except Exception as e:
        print(f"Error accessing microphone: {e}")
        print("Try running with --test flag for testing without microphone.")
        return None

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

async def main(test_mode=False, mic_index=None):
    print("AI Voice Note Summarizer (LLM Version with MAF)")
    print("=" * 50)

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

    # Record audio
    audio = record_audio(duration=10, test_mode=test_mode, mic_index=mic_index)

    # Transcribe
    print("Transcribing...")
    if test_mode or audio is None:
        # Use sample transcription for testing
        transcription = "This is a test voice note. I need to remember to call John about the project deadline. The meeting is scheduled for tomorrow at 2 PM. We discussed the budget allocation and decided to increase the marketing spend by 20 percent. Action items include preparing the presentation slides and sending the agenda to all participants."
        print("Using test transcription (no microphone available)")
    else:
        transcription = transcribe_audio(audio)

    print(f"Transcription: {transcription}")

    if transcription in ["Could not understand audio", ""]:
        print("No valid transcription to summarize.")
        return

    # Summarize using the agent
    print("Summarizing with AI...")
    prompt = f"Please summarize the following voice note transcription:\n\n{transcription}"
    result = await agent.run(prompt)
    print(f"AI Summary: {result.text}")

if __name__ == "__main__":
    import sys
    test_mode = "--test" in sys.argv

    # Check for microphone index
    mic_index = None
    if "--mic" in sys.argv:
        try:
            mic_idx = sys.argv.index("--mic")
            if mic_idx + 1 < len(sys.argv):
                mic_index = int(sys.argv[mic_idx + 1])
        except (ValueError, IndexError):
            print("Invalid microphone index. Use --mic <number>")
            sys.exit(1)

    asyncio.run(main(test_mode=test_mode, mic_index=mic_index))