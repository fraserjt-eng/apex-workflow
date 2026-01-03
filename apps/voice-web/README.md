# Claude Voice Web

Browser-based voice chat with Claude. Uses native Web Speech APIs - no external speech services needed.

## How It Works

```
Your Voice -> [Browser Speech Recognition] -> Text -> [WebSocket] -> [Claude API] -> Response -> [Browser Speech Synthesis] -> Audio
```

Hold the microphone button, speak, release. Claude's response appears on screen and is read aloud.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Run the server
python app.py

# 4. Open in browser
# http://localhost:8000
```

## Requirements

| Requirement | Source | Cost |
|-------------|--------|------|
| Anthropic API Key | [console.anthropic.com](https://console.anthropic.com) | ~$0.003/conversation |
| Chrome or Edge browser | - | Free (for Web Speech API support) |

That's it! Speech recognition and synthesis are handled by your browser for free.

## Browser Compatibility

| Browser | Speech Recognition | Speech Synthesis |
|---------|-------------------|------------------|
| Chrome | Yes | Yes |
| Edge | Yes | Yes |
| Safari | Partial | Yes |
| Firefox | No | Yes |

Chrome or Edge recommended for best experience.

## Features

- **Push-to-talk**: Hold button to speak, release to send
- **Conversation history**: Context maintained throughout session
- **Dark theme**: Easy on the eyes
- **Mobile friendly**: Works on touch devices
- **Auto-reconnect**: WebSocket reconnects if connection drops

## API Usage

The web version only needs your Anthropic API key. Speech recognition and synthesis are handled entirely by your browser's built-in Web Speech APIs.

Typical conversation cost: ~$0.003 (Claude API only)

## Troubleshooting

### "Speech recognition not supported"
Use Chrome or Edge browser. Firefox and some Safari versions don't support Web Speech Recognition.

### "Microphone access denied"
- Click the lock icon in the address bar
- Allow microphone access for this site
- Refresh the page

### No audio output
- Check your system volume
- Make sure your browser isn't muted
- Some browsers need user interaction before playing audio

### WebSocket disconnects
- The app will auto-reconnect after 3 seconds
- Check that the server is still running
- Check browser console for errors

## Development

```bash
# Run with auto-reload
uvicorn app:app --reload --port 8000
```

## How Speech APIs Work

**Speech Recognition (STT)**
Your browser's built-in speech recognition converts your voice to text. This happens locally in Chrome/Edge with some processing on Google/Microsoft servers (depending on browser).

**Speech Synthesis (TTS)**
Your browser converts Claude's text response to spoken audio using system voices. This is entirely local - no external API calls.
