# Claude Voice CLI

Have spoken conversations with Claude using your voice.

## How It Works

```
Your Voice -> [Speech-to-Text] -> Text -> [Claude API] -> Response -> [Text-to-Speech] -> Audio
```

Press Enter to start recording, speak, press Enter again to send. Claude's response is spoken aloud.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API keys
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Run
python main.py
```

## Requirements

| Requirement | Source | Cost |
|-------------|--------|------|
| Anthropic API Key | [console.anthropic.com](https://console.anthropic.com) | ~$0.003/conversation |
| OpenAI API Key (optional) | [platform.openai.com](https://platform.openai.com) | ~$0.006/min audio |
| ElevenLabs Key (optional) | [elevenlabs.io](https://elevenlabs.io) | Free tier available |

## Usage

### Basic Conversation
```bash
python main.py
```

### Test Setup
```bash
python main.py --test
```

### List Available Voices
```bash
python main.py --voice
```

### List Audio Devices
```bash
python main.py --devices
```

### Use Specific Voice
```bash
python main.py --set-voice "com.apple.speech.synthesis.voice.samantha"
```

## In-Session Commands

| Command | Action |
|---------|--------|
| `quit` or `exit` | End the session |
| `clear` | Reset conversation history |
| `history` | Show message count |
| (type text) | Send as text instead of voice |

## Speech-to-Text Options

1. **OpenAI Whisper** (recommended) - Set `OPENAI_API_KEY` in `.env`
2. **Google Speech Recognition** (free fallback) - No API key needed

## Text-to-Speech Options

1. **ElevenLabs** (best quality) - Set `ELEVENLABS_API_KEY` in `.env`
2. **pyttsx3** (offline, free) - Uses system voices, no API key needed

## Troubleshooting

### "No audio recorded"
- Check microphone permissions in System Preferences
- Run `python main.py --devices` to see available inputs
- Run `python main.py --test` to test microphone

### "Could not understand"
- Speak clearly and closer to the microphone
- Check for background noise
- Try speaking slightly slower

### macOS-specific
If you get audio permission errors:
```bash
# Grant terminal access to microphone in System Preferences > Security & Privacy > Microphone
```

## Latency

Expect 2-4 seconds between finishing your sentence and hearing Claude respond. This is normal - we're chaining multiple API calls.
