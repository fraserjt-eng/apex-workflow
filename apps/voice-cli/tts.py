"""
Text-to-speech module.
Supports pyttsx3 (offline) and ElevenLabs (optional, higher quality).
"""

import os
from typing import Optional, List

# Try to import pyttsx3 for offline TTS
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

# Try to import ElevenLabs
try:
    from elevenlabs import generate, play, set_api_key, voices
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False


class TextToSpeech:
    """Handles text-to-speech with multiple backends."""

    def __init__(self, voice_id: Optional[str] = None):
        self.voice_id = voice_id
        self.engine = None
        self.backend = self._detect_backend()

    def _detect_backend(self) -> str:
        """Detect which TTS backend to use."""
        elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")

        if ELEVENLABS_AVAILABLE and elevenlabs_key:
            set_api_key(elevenlabs_key)
            return "elevenlabs"
        elif PYTTSX3_AVAILABLE:
            self.engine = pyttsx3.init()
            # Set default properties for more natural speech
            self.engine.setProperty('rate', 175)  # Slightly slower for clarity
            return "pyttsx3"
        else:
            raise RuntimeError(
                "No TTS backend available. Install pyttsx3 or elevenlabs."
            )

    def speak(self, text: str) -> None:
        """Speak the given text aloud."""
        if self.backend == "elevenlabs":
            self._speak_elevenlabs(text)
        else:
            self._speak_pyttsx3(text)

    def _speak_pyttsx3(self, text: str) -> None:
        """Speak using pyttsx3 (offline)."""
        if self.voice_id:
            self.engine.setProperty('voice', self.voice_id)
        self.engine.say(text)
        self.engine.runAndWait()

    def _speak_elevenlabs(self, text: str) -> None:
        """Speak using ElevenLabs API."""
        try:
            voice = self.voice_id or "Rachel"  # Default to Rachel voice
            audio = generate(
                text=text,
                voice=voice,
                model="eleven_monolingual_v1"
            )
            play(audio)
        except Exception as e:
            print(f"ElevenLabs error: {e}")
            # Fallback to pyttsx3 if available
            if PYTTSX3_AVAILABLE:
                print("Falling back to offline TTS...")
                if not self.engine:
                    self.engine = pyttsx3.init()
                self.engine.say(text)
                self.engine.runAndWait()

    def list_voices(self) -> List[dict]:
        """List available voices for the current backend."""
        if self.backend == "elevenlabs":
            return self._list_elevenlabs_voices()
        else:
            return self._list_pyttsx3_voices()

    def _list_pyttsx3_voices(self) -> List[dict]:
        """List available pyttsx3 voices."""
        voice_list = []
        for voice in self.engine.getProperty('voices'):
            voice_list.append({
                'id': voice.id,
                'name': voice.name,
                'languages': getattr(voice, 'languages', []),
            })
        return voice_list

    def _list_elevenlabs_voices(self) -> List[dict]:
        """List available ElevenLabs voices."""
        try:
            available_voices = voices()
            return [
                {'id': v.voice_id, 'name': v.name}
                for v in available_voices
            ]
        except Exception as e:
            print(f"Error listing ElevenLabs voices: {e}")
            return []

    def set_voice(self, voice_id: str) -> None:
        """Set the voice to use for TTS."""
        self.voice_id = voice_id
        if self.backend == "pyttsx3" and self.engine:
            self.engine.setProperty('voice', voice_id)

    def get_backend_name(self) -> str:
        """Return the name of the active TTS backend."""
        if self.backend == "elevenlabs":
            return "ElevenLabs"
        else:
            return "pyttsx3 (offline)"


def print_available_voices() -> None:
    """Print all available voices."""
    tts = TextToSpeech()
    print(f"\nUsing TTS backend: {tts.get_backend_name()}")
    print("-" * 50)

    voices_list = tts.list_voices()
    if not voices_list:
        print("No voices found.")
        return

    for voice in voices_list:
        print(f"  ID: {voice['id']}")
        print(f"  Name: {voice['name']}")
        if 'languages' in voice and voice['languages']:
            print(f"  Languages: {voice['languages']}")
        print()
