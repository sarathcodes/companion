<p align="center">
  <img src="static/logo.png" style="width: 500px;">
</p>

# Companion: Gemini-Powered Foreign-Language Private Tutor

![demo](docs/images/demo.gif)

![Supports Python 3.10 and above](https://img.shields.io/badge/Python-%3E=3.10-green?style=for-the-badge)
[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-blue?style=for-the-badge)](https://creativecommons.org/licenses/by-nc/4.0/)

Companion is an AI-powered foreign-language private tutor ported to run entirely on a single **Google AI Studio (`GEMINI_API_KEY`)** key using the **Google GenAI SDK (`google-genai`)**:
- **Conversational Tutor**: `gemini-3.8-flash` via the Gemini Interactions API with server-side multi-turn state and streaming
- **Speech-to-Text (STT)**: `gemini-3.5-transcribe` for voice recording transcription and automatic language detection
- **Text-to-Speech (TTS)**: `gemini-3.8-flash-lite-tts` with Gemini's prebuilt studio voices (`Kore`, `Puck`, `Aoede`, etc.)
- **Translation & Language Detection**: `gemini-3.5-flash-lite`

No separate OpenAI account or Google Cloud Service Account is required.

## Quick Start

1. **Get a Gemini API Key** from [Google AI Studio](https://aistudio.google.com/apikey).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your API key and run**:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   python companion.py
   ```
4. Open `http://127.0.0.1:5000` in your browser (or `http://127.0.0.1:5000/setup` to customize your tutor, voice, and language).

---

[Companion Licences](/docs/licenses.md)
