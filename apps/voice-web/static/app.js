/**
 * Claude Voice Web - Frontend Application
 *
 * Uses Web Speech API for speech recognition and synthesis.
 * Communicates with backend via WebSocket.
 */

class VoiceChat {
    constructor() {
        // DOM elements
        this.micBtn = document.getElementById('mic-btn');
        this.micLabel = document.getElementById('mic-label');
        this.conversation = document.getElementById('conversation');
        this.connectionStatus = document.getElementById('connection-status');
        this.clearBtn = document.getElementById('clear-btn');

        // State
        this.isRecording = false;
        this.isProcessing = false;
        this.ws = null;
        this.sessionId = this.generateSessionId();

        // Speech APIs
        this.recognition = null;
        this.synthesis = window.speechSynthesis;

        // Initialize
        this.init();
    }

    generateSessionId() {
        return 'session_' + Math.random().toString(36).substring(2, 15);
    }

    init() {
        // Check for speech recognition support
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.showError('Speech recognition not supported in this browser. Try Chrome or Edge.');
            return;
        }

        // Initialize speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';

        // Recognition events
        this.recognition.onresult = (event) => this.handleRecognitionResult(event);
        this.recognition.onerror = (event) => this.handleRecognitionError(event);
        this.recognition.onend = () => this.handleRecognitionEnd();

        // Connect WebSocket
        this.connectWebSocket();

        // Button events
        this.micBtn.addEventListener('mousedown', () => this.startRecording());
        this.micBtn.addEventListener('mouseup', () => this.stopRecording());
        this.micBtn.addEventListener('mouseleave', () => {
            if (this.isRecording) this.stopRecording();
        });

        // Touch events for mobile
        this.micBtn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.startRecording();
        });
        this.micBtn.addEventListener('touchend', (e) => {
            e.preventDefault();
            this.stopRecording();
        });

        // Clear button
        this.clearBtn.addEventListener('click', () => this.clearConversation());

        // Cancel any ongoing speech when page unloads
        window.addEventListener('beforeunload', () => {
            this.synthesis.cancel();
        });
    }

    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/${this.sessionId}`;

        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            this.updateConnectionStatus('connected', 'Connected');
            this.micBtn.disabled = false;
        };

        this.ws.onclose = () => {
            this.updateConnectionStatus('disconnected', 'Disconnected');
            this.micBtn.disabled = true;
            // Attempt reconnection after 3 seconds
            setTimeout(() => this.connectWebSocket(), 3000);
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus('disconnected', 'Connection Error');
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleServerMessage(data);
        };
    }

    updateConnectionStatus(className, text) {
        this.connectionStatus.className = `status ${className}`;
        this.connectionStatus.textContent = text;
    }

    startRecording() {
        if (this.isRecording || this.isProcessing) return;

        // Stop any ongoing speech
        this.synthesis.cancel();

        this.isRecording = true;
        this.micBtn.classList.add('recording');
        this.micLabel.textContent = 'Listening...';
        this.updateConnectionStatus('listening', 'Listening');

        try {
            this.recognition.start();
        } catch (e) {
            console.error('Recognition start error:', e);
            this.stopRecording();
        }
    }

    stopRecording() {
        if (!this.isRecording) return;

        this.isRecording = false;
        this.micBtn.classList.remove('recording');
        this.micLabel.textContent = 'Processing...';

        try {
            this.recognition.stop();
        } catch (e) {
            console.error('Recognition stop error:', e);
        }
    }

    handleRecognitionResult(event) {
        const transcript = event.results[0][0].transcript;

        if (transcript.trim()) {
            this.addMessage('user', transcript);
            this.sendToServer(transcript);
        }
    }

    handleRecognitionError(event) {
        console.error('Speech recognition error:', event.error);

        if (event.error === 'no-speech') {
            this.showError('No speech detected. Try again.');
        } else if (event.error === 'not-allowed') {
            this.showError('Microphone access denied. Please allow microphone access.');
        } else {
            this.showError(`Recognition error: ${event.error}`);
        }

        this.resetMicButton();
    }

    handleRecognitionEnd() {
        if (!this.isProcessing) {
            this.resetMicButton();
        }
    }

    resetMicButton() {
        this.isRecording = false;
        this.isProcessing = false;
        this.micBtn.classList.remove('recording', 'processing');
        this.micLabel.textContent = 'Hold to Speak';
        this.updateConnectionStatus('connected', 'Connected');
    }

    sendToServer(text) {
        this.isProcessing = true;
        this.micBtn.classList.add('processing');
        this.micLabel.textContent = 'Thinking...';

        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'transcription',
                text: text
            }));
        } else {
            this.showError('Not connected to server');
            this.resetMicButton();
        }
    }

    handleServerMessage(data) {
        switch (data.type) {
            case 'response':
                this.addMessage('assistant', data.text);
                this.speak(data.text);
                this.resetMicButton();
                break;

            case 'error':
                this.showError(data.message);
                this.resetMicButton();
                break;

            case 'cleared':
                this.conversation.innerHTML = `
                    <div class="welcome-message">
                        <p>Conversation cleared. Start fresh!</p>
                    </div>
                `;
                break;

            case 'pong':
                // Connection alive
                break;
        }
    }

    addMessage(role, text) {
        // Remove welcome message if present
        const welcome = this.conversation.querySelector('.welcome-message');
        if (welcome) welcome.remove();

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        messageDiv.textContent = text;
        this.conversation.appendChild(messageDiv);

        // Scroll to bottom
        this.conversation.scrollTop = this.conversation.scrollHeight;
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message error';
        errorDiv.textContent = message;
        this.conversation.appendChild(errorDiv);
        this.conversation.scrollTop = this.conversation.scrollHeight;

        // Remove after 5 seconds
        setTimeout(() => errorDiv.remove(), 5000);
    }

    speak(text) {
        // Cancel any ongoing speech
        this.synthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;

        // Try to use a natural voice
        const voices = this.synthesis.getVoices();
        const preferredVoice = voices.find(v =>
            v.name.includes('Samantha') ||
            v.name.includes('Google') ||
            v.name.includes('Natural') ||
            v.lang.startsWith('en')
        );

        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }

        this.synthesis.speak(utterance);
    }

    clearConversation() {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ type: 'clear' }));
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Load voices (needed for some browsers)
    if (window.speechSynthesis) {
        window.speechSynthesis.getVoices();
        window.speechSynthesis.onvoiceschanged = () => {
            window.speechSynthesis.getVoices();
        };
    }

    new VoiceChat();
});
