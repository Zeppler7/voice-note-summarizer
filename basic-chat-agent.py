import os
import asyncio
import requests
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

async def main():
    chat_client = PuterClient(
        auth_token=PUTER_AUTH_TOKEN,
        model=PUTER_MODEL
    )

    agent = ChatAgent(
        chat_client=chat_client,
        instructions="You are a helpful assistant that keeps track of my day ",
        name="Daily Life tracker"
        )
    
    result = await agent.run("My name is John and I love hiking.")
    print("Agent Response:", result.text)

    result = await agent.run("What's my name?")
    print("Agent Response:", result.text)

if __name__ == "__main__":
    asyncio.run(main())