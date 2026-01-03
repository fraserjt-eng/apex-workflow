"""
Claude Voice Web - FastAPI backend for browser-based voice chat.

Run with: python app.py
Then open: http://localhost:8000
"""

import os
import json
from typing import Dict, List
from dataclasses import dataclass, field

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from anthropic import Anthropic

# Initialize FastAPI app
app = FastAPI(title="Claude Voice Web")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Claude client
anthropic_client = None


def get_client() -> Anthropic:
    """Get or create Anthropic client."""
    global anthropic_client
    if anthropic_client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment")
        anthropic_client = Anthropic(api_key=api_key)
    return anthropic_client


# Session storage (in-memory)
sessions: Dict[str, List[dict]] = {}

# System prompt for voice mode
SYSTEM_PROMPT = (
    "You are Claude in voice conversation mode. Keep responses concise and "
    "conversational - aim for 1-3 sentences unless the user asks for detail. "
    "Be warm and natural."
)


@app.get("/")
async def root():
    """Serve the main page."""
    return FileResponse("static/index.html")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "message": "Claude Voice Web is running"}


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for voice chat.

    Receives transcribed text from browser, sends to Claude, returns response.
    """
    await websocket.accept()

    # Initialize session if new
    if session_id not in sessions:
        sessions[session_id] = []

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "transcription":
                user_text = message.get("text", "").strip()

                if not user_text:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Empty transcription received"
                    })
                    continue

                # Add user message to history
                sessions[session_id].append({
                    "role": "user",
                    "content": user_text
                })

                # Send to Claude
                try:
                    client = get_client()
                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1024,
                        system=SYSTEM_PROMPT,
                        messages=sessions[session_id]
                    )

                    assistant_text = response.content[0].text

                    # Add assistant response to history
                    sessions[session_id].append({
                        "role": "assistant",
                        "content": assistant_text
                    })

                    # Send response to client
                    await websocket.send_json({
                        "type": "response",
                        "text": assistant_text
                    })

                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Claude API error: {str(e)}"
                    })

            elif message.get("type") == "clear":
                # Clear conversation history
                sessions[session_id] = []
                await websocket.send_json({
                    "type": "cleared",
                    "message": "Conversation history cleared"
                })

            elif message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        # Clean up session after disconnect (optional: keep history for reconnection)
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    print(f"\n{'='*50}")
    print("  CLAUDE VOICE WEB")
    print(f"  Open http://localhost:{port} in your browser")
    print(f"{'='*50}\n")

    uvicorn.run(app, host="0.0.0.0", port=port)
