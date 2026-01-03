"""
Speech-to-text transcription module.
Supports OpenAI Whisper API with fallback to Google Speech Recognition.
"""

import os
from typing import Optional

# Try to import OpenAI for Whisper
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Try to import speech_recognition as fallback
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False


class Transcriber:
    """Handles speech-to-text transcription with multiple backends."""

    def __init__(self):
        self.openai_client = None
        self.recognizer = None
        self.backend = self._detect_backend()

    def _detect_backend(self) -> str:
        """Detect which transcription backend to use."""
        openai_key = os.getenv("OPENAI_API_KEY")

        if OPENAI_AVAILABLE and openai_key:
            self.openai_client = OpenAI(api_key=openai_key)
            return "whisper"
        elif SR_AVAILABLE:
            self.recognizer = sr.Recognizer()
            return "google"
        else:
            raise RuntimeError(
                "No transcription backend available. Install openai or speech_recognition."
            )

    def transcribe(self, audio_bytes: bytes, filepath: Optional[str] = None) -> Optional[str]:
        """
        Transcribe audio to text.

        Args:
            audio_bytes: WAV audio data as bytes
            filepath: Optional path to save audio file (required for Whisper)

        Returns:
            Transcribed text or None if failed
        """
        if self.backend == "whisper":
            return self._transcribe_whisper(audio_bytes, filepath)
        else:
            return self._transcribe_google(audio_bytes)

    def _transcribe_whisper(self, audio_bytes: bytes, filepath: Optional[str] = None) -> Optional[str]:
        """Transcribe using OpenAI Whisper API."""
        import tempfile
        from pathlib import Path

        # Write to temp file if no filepath provided
        if filepath is None:
            temp_dir = tempfile.gettempdir()
            filepath = str(Path(temp_dir) / "whisper_input.wav")

        # Save audio bytes to file
        with open(filepath, 'wb') as f:
            f.write(audio_bytes)

        try:
            with open(filepath, 'rb') as audio_file:
                response = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return response.strip() if response else None

        except Exception as e:
            print(f"Whisper transcription error: {e}")
            return None

    def _transcribe_google(self, audio_bytes: bytes) -> Optional[str]:
        """Transcribe using Google Speech Recognition (free, no API key)."""
        import io
        import wave

        if not self.recognizer:
            self.recognizer = sr.Recognizer()

        try:
            # Convert bytes to AudioData
            wav_io = io.BytesIO(audio_bytes)
            with wave.open(wav_io, 'rb') as wav_file:
                sample_rate = wav_file.getframerate()
                sample_width = wav_file.getsampwidth()
                audio_data = wav_file.readframes(wav_file.getnframes())

            audio = sr.AudioData(audio_data, sample_rate, sample_width)

            # Use Google's free speech recognition
            text = self.recognizer.recognize_google(audio)
            return text

        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Google Speech Recognition error: {e}")
            return None
        except Exception as e:
            print(f"Transcription error: {e}")
            return None

    def get_backend_name(self) -> str:
        """Return the name of the active transcription backend."""
        if self.backend == "whisper":
            return "OpenAI Whisper"
        else:
            return "Google Speech Recognition"
