"""
Audio recording and playback module for voice CLI.
Handles microphone input capture and audio file management.
"""

import io
import wave
import tempfile
from pathlib import Path
from typing import Optional

import sounddevice as sd
import soundfile as sf
import numpy as np


class AudioRecorder:
    """Push-to-talk audio recorder using sounddevice."""

    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_data: list[np.ndarray] = []

    def start_recording(self) -> None:
        """Start recording audio from the default microphone."""
        self.recording = True
        self.audio_data = []

        def callback(indata, frames, time, status):
            if status:
                print(f"Audio status: {status}")
            if self.recording:
                self.audio_data.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='float32',
            callback=callback
        )
        self.stream.start()

    def stop_recording(self) -> Optional[bytes]:
        """Stop recording and return audio data as WAV bytes."""
        self.recording = False

        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()

        if not self.audio_data:
            return None

        # Concatenate all recorded chunks
        audio = np.concatenate(self.audio_data, axis=0)

        # Convert to WAV bytes
        wav_buffer = io.BytesIO()
        sf.write(wav_buffer, audio, self.sample_rate, format='WAV')
        wav_buffer.seek(0)

        return wav_buffer.read()

    def save_to_file(self, audio_bytes: bytes, filepath: str) -> str:
        """Save audio bytes to a WAV file."""
        with open(filepath, 'wb') as f:
            f.write(audio_bytes)
        return filepath

    def get_temp_filepath(self) -> str:
        """Get a temporary file path for audio."""
        temp_dir = tempfile.gettempdir()
        return str(Path(temp_dir) / "voice_cli_recording.wav")


def list_audio_devices() -> None:
    """Print available audio input devices."""
    print("\nAvailable audio devices:")
    print("-" * 50)
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            marker = " (default)" if i == sd.default.device[0] else ""
            print(f"  [{i}] {device['name']}{marker}")
    print()


def test_microphone(duration: float = 2.0) -> bool:
    """Test microphone by recording briefly and checking for audio."""
    print(f"Testing microphone for {duration} seconds...")
    try:
        recording = sd.rec(
            int(duration * 16000),
            samplerate=16000,
            channels=1,
            dtype='float32'
        )
        sd.wait()

        # Check if we got any significant audio
        max_amplitude = np.max(np.abs(recording))
        if max_amplitude > 0.01:
            print(f"Microphone working! Peak amplitude: {max_amplitude:.3f}")
            return True
        else:
            print("Warning: Very low audio level. Check microphone.")
            return True  # Still technically working

    except Exception as e:
        print(f"Microphone test failed: {e}")
        return False
