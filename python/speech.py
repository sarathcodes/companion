import os
import re
import base64
import asyncio
import edge_tts
from google import genai
from typing import Dict, List, Optional
from python.config import Config
from python.consts import (
    DEFAULT_STT_MODEL,
    GEMINI_FEMALE_VOICES,
    GEMINI_MALE_VOICES,
    SUPPORTED_OUTPUT_LOCALES,
)

gemini_client: Optional[genai.Client] = None
default_voice: str = "Kore"
default_gender: str = "female"
default_learning_lang: str = "fr"

# Map language ISO codes to natural neural voices (female, male)
LOCALE_NEURAL_VOICES = {
    "fr": ("fr-FR-VivienneMultilingualNeural", "fr-FR-RemyMultilingualNeural"),
    "es": ("es-ES-ElviraNeural", "es-ES-AlvaroNeural"),
    "de": ("de-DE-SeraphinaMultilingualNeural", "de-DE-FlorianMultilingualNeural"),
    "it": ("it-IT-ElsaNeural", "it-IT-DiegoNeural"),
    "pt": ("pt-BR-ThalitaMultilingualNeural", "pt-BR-AntonioNeural"),
    "en": ("en-US-avaMultilingualNeural", "en-US-AndrewMultilingualNeural"),
    "nl": ("nl-NL-ColetteNeural", "nl-NL-MaartenNeural"),
    "ru": ("ru-RU-SvetlanaNeural", "ru-RU-DmitryNeural"),
    "ja": ("ja-JP-NanamiNeural", "ja-JP-KeitaNeural"),
    "ko": ("ko-KR-SunHiNeural", "ko-KR-InJoonNeural"),
    "zh": ("zh-CN-XiaoxiaoNeural", "zh-CN-YunxiNeural"),
    "ar": ("ar-SA-ZariyahNeural", "ar-SA-HamedNeural"),
    "hi": ("hi-IN-SwaraNeural", "hi-IN-MadhurNeural"),
}


def init_speech(config: Config, client: genai.Client) -> None:
    """
    Initialize speech-to-text and text-to-speech configuration

    :param config: Config
    :param client: a Google GenAI Client object
    """
    global gemini_client, default_voice, default_gender, default_learning_lang

    gemini_client = client
    bot_cfg = config.get("bot", {}) if config else {}
    lang_cfg = config.get("language", {}) if config else {}
    default_voice = bot_cfg.get("voice", "Kore") or "Kore"
    default_gender = (bot_cfg.get("gender", "female") or "female").lower()
    default_learning_lang = (lang_cfg.get("learning", "fr") or "fr").split("-")[0].lower()


def get_voice_object(voice_name: str, language_code: Optional[str] = None) -> str:
    """
    Resolve a voice identifier for TTS synthesis.
    """
    if voice_name and "Neural" in voice_name:
        return voice_name
    lang_prefix = (language_code or default_learning_lang or "fr").split("-")[0].lower()
    female_neural, male_neural = LOCALE_NEURAL_VOICES.get(
        lang_prefix, ("fr-FR-VivienneMultilingualNeural", "fr-FR-RemyMultilingualNeural")
    )
    if voice_name in GEMINI_MALE_VOICES or default_gender == "male":
        return male_neural
    return female_neural


def speech2text(filename: str, language: Optional[str] = None) -> str:
    """
    Convert audio file containing user recording to text using Gemini 3.5 Transcribe

    :param filename: mp3 filename with recording
    :param language: ISO 639-1 or BCP-47 code of the language spoken in the recording.
                     If None, Gemini 3.5 Transcribe detects the language automatically.
    :return: transcribed text
    """
    with open(filename, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")

    language_codes: List[str] = []
    if language:
        matched_locales = [loc for loc in SUPPORTED_OUTPUT_LOCALES if loc.lower().startswith(f"{language.lower()}-")]
        if matched_locales:
            language_codes = [matched_locales[0]]
        elif "-" in language:
            language_codes = [language]

    response = gemini_client.interactions.create(
        model=DEFAULT_STT_MODEL,
        input=[{
            "type": "audio",
            "data": audio_b64,
            "mime_type": "audio/mp3",
        }],
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
    Convert text to speech using neural TTS (`edge-tts`) for sub-second, quota-free synthesis.

    :param text: text to be converted
    :param filename: mp3 file path to save the synthesized speech audio
    :param voice: an optional alternative voice name, instead of the default one
    :return: filename if audio was generated, or empty string if skipped
    """
    clean_text = re.sub(r"[*_#`~]+", "", text or "")
    clean_text = re.sub(r"\s+", " ", clean_text).strip()
    if not clean_text or not any(c.isalnum() for c in clean_text):
        return ""

    neural_voice = get_voice_object(voice or default_voice)
    asyncio.run(edge_tts.Communicate(clean_text, neural_voice).save(filename))
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        return filename
    return ""


def voices_by_features() -> Dict[str, Dict[str, List[str]]]:
    """
    Return voices supported by TTS, organized by language locale and gender.

    :return: Dict: {lang_locale: {gender: [list of voices]}}
    """
    voices_dict: Dict[str, Dict[str, List[str]]] = {}
    for locale in SUPPORTED_OUTPUT_LOCALES:
        voices_dict[locale] = {
            "female": list(GEMINI_FEMALE_VOICES),
            "male": list(GEMINI_MALE_VOICES),
        }
    return voices_dict
