import os
import re
import base64
from google import genai
from typing import Dict, List, Optional
from python.config import Config
from python.consts import (
    DEFAULT_STT_MODEL,
    DEFAULT_TTS_MODEL,
    GEMINI_FEMALE_VOICES,
    GEMINI_MALE_VOICES,
    SUPPORTED_OUTPUT_LOCALES,
)

gemini_client: Optional[genai.Client] = None
default_voice: str = "Kore"


def init_speech(config: Config, client: genai.Client) -> None:
    """
    Initialize Gemini client and default voice for speech-to-text and text-to-speech

    :param config: Config
    :param client: a Google GenAI Client object
    """
    global gemini_client, default_voice

    gemini_client = client
    configured_voice = config.get("bot", {}).get("voice", "Kore") if config else "Kore"
    default_voice = get_voice_object(voice_name=configured_voice)


def get_voice_object(voice_name: str, language_code: Optional[str] = None) -> str:
    """
    Normalize a voice name for Gemini TTS.
    Falls back to 'Kore' if a legacy Google Cloud TTS placeholder (e.g. 'xx-xx' or 'fr-FR-Neural2-A') is provided.

    :param voice_name: voice name (e.g. 'Kore', 'Puck', or 'voice_...')
    :param language_code: optional language code (unused, as Gemini 3.8 TTS detects language automatically)
    :return: normalized voice name string
    """
    if not voice_name or ("-" in voice_name and not voice_name.startswith("voice_")):
        return "Kore"
    return voice_name


def speech2text(filename: str, language: Optional[str] = None) -> str:
    """
    Convert audio file containing user recording to text using Gemini 3.5 Transcribe

    :param filename: audio filename with recording
    :param language: ISO 639-1 or BCP-47 code of the language spoken in the recording.
                     If None, Gemini 3.5 Transcribe detects the language automatically.
    :return: transcribed text
    """
    audio_file = gemini_client.files.upload(file=filename)
    language_codes: List[str] = []
    if language:
        matched_locales = [loc for loc in SUPPORTED_OUTPUT_LOCALES if loc.lower().startswith(f"{language.lower()}-")]
        if matched_locales:
            language_codes = [matched_locales[0]]
        elif "-" in language:
            language_codes = [language]

    response = gemini_client.interactions.create(
        model=DEFAULT_STT_MODEL,
        input=[audio_file],
        generation_config={
            "transcription_config": {
                "language_codes": language_codes,
            }
        },
        store=False,
    )
    return (response.output_text or "").strip()


def text2speech(text: str, filename: str, voice: Optional[str] = None) -> str:
    """
    Convert text to speech using Gemini 3.8 TTS (`gemini-3.8-flash-lite-tts`)

    :param text: text to be converted
    :param filename: file path to save the synthesized speech audio (WAV format, decoded natively by Web Audio API)
    :param voice: an optional alternative voice name, instead of the default one
    :return: filename if audio was generated, or empty string if skipped
    """
    # Strip markdown formatting characters and normalize whitespace before TTS synthesis
    clean_text = re.sub(r"[*_#`~]+", "", text or "")
    clean_text = re.sub(r"\s+", " ", clean_text).strip()
    if not clean_text or not any(c.isalnum() for c in clean_text):
        return ""

    selected_voice = get_voice_object(voice or default_voice)
    interaction = gemini_client.interactions.create(
        model=DEFAULT_TTS_MODEL,
        input=[{
            "type": "user_input",
            "content": [{
                "type": "text",
                "text": clean_text,
                "annotations": [{
                    "type": "speech_metadata",
                    "style": "warm, clear, and natural language tutor",
                }],
            }],
        }],
        response_format={"type": "audio"},
        generation_config={
            "speech_config": [
                {"voice": selected_voice},
            ]
        },
        store=False,
    )

    if interaction.output_audio and interaction.output_audio.data:
        audio_bytes = base64.b64decode(interaction.output_audio.data)
        with open(filename, "wb") as audio_file:
            audio_file.write(audio_bytes)
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            return filename
    return ""


def voices_by_features() -> Dict[str, Dict[str, List[str]]]:
    """
    Return voices supported by Gemini 3.8 TTS, organized by language locale and gender.

    :return: Dict: {lang_locale: {gender: [list of voices]}}
    """
    voices_dict: Dict[str, Dict[str, List[str]]] = {}
    for locale in SUPPORTED_OUTPUT_LOCALES:
        voices_dict[locale] = {
            "female": list(GEMINI_FEMALE_VOICES),
            "male": list(GEMINI_MALE_VOICES),
        }
    return voices_dict
