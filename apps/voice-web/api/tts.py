"""
Text-to-Speech API using edge-tts with ChristopherNeural voice
"""

import json
import base64
import asyncio
from http.server import BaseHTTPRequestHandler

import edge_tts

# Voice configuration - same as audiobook generator
VOICE = "en-US-ChristopherNeural"
RATE = "-5%"


async def generate_speech(text: str) -> bytes:
    """Generate speech audio from text using edge-tts"""
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)

    # Collect audio chunks
    audio_chunks = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])

    return b"".join(audio_chunks)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            text = data.get("text", "").strip()

            if not text:
                self.send_error_response(400, "No text provided")
                return

            # Generate audio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            audio_bytes = loop.run_until_complete(generate_speech(text))
            loop.close()

            # Return audio as base64
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            response_data = {
                "audio": audio_base64,
                "format": "mp3"
            }
            self.wfile.write(json.dumps(response_data).encode())

        except Exception as e:
            self.send_error_response(500, str(e))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())
