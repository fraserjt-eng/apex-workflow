"""
Claude Voice Web - Vercel Serverless API
HTTP POST endpoint for voice chat (WebSocket alternative for serverless)
"""

import os
import json
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

# System prompt for voice mode
SYSTEM_PROMPT = (
    "You are Claude in voice conversation mode. Keep responses concise and "
    "conversational - aim for 1-3 sentences unless the user asks for detail. "
    "Be warm and natural."
)

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get API key (strip whitespace/newlines)
            api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
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

            # Call Claude API directly with urllib (no external deps)
            request_data = json.dumps({
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1024,
                "system": SYSTEM_PROMPT,
                "messages": messages
            }).encode('utf-8')

            req = urllib.request.Request(
                ANTHROPIC_API_URL,
                data=request_data,
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01"
                }
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))

            assistant_text = result["content"][0]["text"]

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
            import traceback
            error_detail = f"{type(e).__name__}: {str(e)}"
            print(f"Error: {error_detail}")
            print(traceback.format_exc())
            self.send_error_response(500, error_detail)

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
