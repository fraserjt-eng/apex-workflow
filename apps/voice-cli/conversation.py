"""
Conversation management module.
Handles Claude API calls and conversation history.
"""

import os
from typing import List, Optional
from dataclasses import dataclass, field

from anthropic import Anthropic


@dataclass
class Message:
    """Represents a single message in the conversation."""
    role: str  # "user" or "assistant"
    content: str


@dataclass
class Conversation:
    """Manages conversation state and Claude API interactions."""

    system_prompt: str = (
        "You are Claude in voice conversation mode. Keep responses concise and "
        "conversational - aim for 1-3 sentences unless the user asks for detail. "
        "Be warm and natural."
    )
    model: str = "claude-sonnet-4-20250514"
    messages: List[Message] = field(default_factory=list)
    client: Optional[Anthropic] = None

    def __post_init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not set. Add it to your .env file."
            )
        self.client = Anthropic(api_key=api_key)

    def add_user_message(self, content: str) -> None:
        """Add a user message to the conversation history."""
        self.messages.append(Message(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to the conversation history."""
        self.messages.append(Message(role="assistant", content=content))

    def get_response(self, user_input: str) -> str:
        """
        Send user input to Claude and get a response.

        Args:
            user_input: The user's transcribed speech

        Returns:
            Claude's response text
        """
        # Add user message to history
        self.add_user_message(user_input)

        # Format messages for API
        api_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=self.system_prompt,
                messages=api_messages
            )

            # Extract text from response
            assistant_text = response.content[0].text

            # Add to history
            self.add_assistant_message(assistant_text)

            return assistant_text

        except Exception as e:
            error_msg = f"Error getting response from Claude: {e}"
            print(error_msg)
            return "I'm sorry, I encountered an error. Could you try again?"

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.messages = []

    def get_history_length(self) -> int:
        """Return the number of messages in history."""
        return len(self.messages)

    def get_last_exchange(self) -> Optional[tuple[str, str]]:
        """Return the last user message and assistant response."""
        if len(self.messages) >= 2:
            return (
                self.messages[-2].content,  # User
                self.messages[-1].content   # Assistant
            )
        return None


def test_connection() -> bool:
    """Test the Claude API connection."""
    try:
        conv = Conversation()
        response = conv.get_response("Say 'connection successful' in exactly those words.")
        print(f"Claude says: {response}")
        return "connection" in response.lower() or "successful" in response.lower()
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False
