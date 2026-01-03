"""
Claude Voice Web - Vercel Serverless API
HTTP POST endpoint for voice chat (WebSocket alternative for serverless)
"""

import os
import json
from http.server import BaseHTTPRequestHandler
from anthropic import Anthropic

# System prompt for voice mode
SYSTEM_PROMPT = (
    "You are Claude in voice conversation mode. Keep responses concise and "
    "conversational - aim for 1-3 sentences unless the user asks for detail. "
    "Be warm and natural."
)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get API key
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                self.send_error_response(500, "ANTHROPIC_API_KEY not configured")
                return

            # Parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            user_text = data.get("text", "").strip()
            history = data.get("history", [])

            if not user_text:
                self.send_error_response(400, "No text provided")
                return

            # Add user message to history
            messages = history + [{"role": "user", "content": user_text}]

            # Call Claude API
            client = Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=messages
            )

            assistant_text = response.content[0].text

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            response_data = {
                "text": assistant_text,
                "history": messages + [{"role": "assistant", "content": assistant_text}]
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
