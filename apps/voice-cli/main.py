#!/usr/bin/env python3
"""
Claude Voice CLI - Have spoken conversations with Claude.

Usage:
    python main.py              Start voice conversation
    python main.py --voice      List available TTS voices
    python main.py --test       Test microphone and API connections
"""

import os
import sys
import argparse
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from audio import AudioRecorder, list_audio_devices, test_microphone
from transcribe import Transcriber
from tts import TextToSpeech, print_available_voices
from conversation import Conversation, test_connection


def print_banner():
    """Print the application banner."""
    print("\n" + "=" * 50)
    print("  CLAUDE VOICE CLI")
    print("  Speak with Claude using your voice")
    print("=" * 50)


def print_instructions():
    """Print usage instructions."""
    print("\nInstructions:")
    print("  - Press ENTER to start recording")
    print("  - Press ENTER again to stop and send")
    print("  - Type 'quit' or 'exit' to end the session")
    print("  - Type 'clear' to reset conversation history")
    print("-" * 50 + "\n")


def wait_for_enter(prompt: str = "") -> str:
    """Wait for user to press Enter or type a command."""
    try:
        return input(prompt).strip().lower()
    except EOFError:
        return "quit"


def main():
    """Main entry point for the voice CLI."""
    parser = argparse.ArgumentParser(
        description="Have voice conversations with Claude"
    )
    parser.add_argument(
        "--voice", "-v",
        action="store_true",
        help="List available TTS voices"
    )
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Test microphone and API connections"
    )
    parser.add_argument(
        "--devices", "-d",
        action="store_true",
        help="List available audio input devices"
    )
    parser.add_argument(
        "--set-voice",
        type=str,
        help="Set the TTS voice ID to use"
    )

    args = parser.parse_args()

    # Handle --devices flag
    if args.devices:
        list_audio_devices()
        return

    # Handle --voice flag
    if args.voice:
        print_available_voices()
        return

    # Handle --test flag
    if args.test:
        print("\nRunning diagnostics...")
        print("-" * 50)

        print("\n1. Testing microphone...")
        mic_ok = test_microphone()

        print("\n2. Testing Claude API connection...")
        api_ok = test_connection()

        print("\n" + "-" * 50)
        print("Results:")
        print(f"  Microphone: {'OK' if mic_ok else 'FAILED'}")
        print(f"  Claude API: {'OK' if api_ok else 'FAILED'}")
        return

    # Main conversation loop
    print_banner()

    # Initialize components
    try:
        print("\nInitializing...")
        recorder = AudioRecorder()
        transcriber = Transcriber()
        tts = TextToSpeech(voice_id=args.set_voice)
        conversation = Conversation()

        print(f"  STT: {transcriber.get_backend_name()}")
        print(f"  TTS: {tts.get_backend_name()}")
        print("  Ready!")

    except Exception as e:
        print(f"\nError initializing: {e}")
        print("\nMake sure you have:")
        print("  1. Created a .env file with your API keys")
        print("  2. Installed all requirements: pip install -r requirements.txt")
        sys.exit(1)

    print_instructions()

    # Conversation loop
    while True:
        # Wait for user to start recording
        command = wait_for_enter("[Press ENTER to speak, or type command] ")

        # Handle commands
        if command in ("quit", "exit", "q"):
            print("\nGoodbye!")
            break
        elif command == "clear":
            conversation.clear_history()
            print("Conversation history cleared.\n")
            continue
        elif command == "history":
            print(f"\nConversation has {conversation.get_history_length()} messages.\n")
            continue
        elif command and command not in ("", "\n"):
            # If user typed something other than Enter, treat as text input
            print(f"\nYou typed: {command}")
            print("Processing...")
            response = conversation.get_response(command)
            print(f"\nClaude: {response}\n")
            tts.speak(response)
            continue

        # Start recording
        print("Recording... (press ENTER to stop)")
        recorder.start_recording()

        # Wait for user to stop recording
        wait_for_enter("")

        # Stop and get audio
        print("Processing...")
        audio_bytes = recorder.stop_recording()

        if not audio_bytes:
            print("No audio recorded. Try again.\n")
            continue

        # Transcribe
        filepath = recorder.get_temp_filepath()
        text = transcriber.transcribe(audio_bytes, filepath)

        if not text:
            print("Could not understand. Please try again.\n")
            continue

        print(f"\nYou said: {text}")

        # Get Claude's response
        response = conversation.get_response(text)
        print(f"\nClaude: {response}\n")

        # Speak the response
        tts.speak(response)


if __name__ == "__main__":
    main()
