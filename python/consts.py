import os

TEMP_DIR_NAME = "tmp"
TEMP_DIR = os.path.join(os.getcwd(), f"static/{TEMP_DIR_NAME}")
LTM_DIR = os.path.join(os.getcwd(), "ltm")  # Long Term Memory
SAVED_SESSION_FILE = os.path.join(LTM_DIR, "last_session.json")

DEFAULT_CHAT_MODEL = "gemini-3.5-flash-lite"
DEFAULT_FAST_MODEL = "gemini-3.5-flash-lite"
DEFAULT_STT_MODEL = "gemini-3.5-transcribe"
DEFAULT_TTS_MODEL = "gemini-3.8-flash-lite-tts"

GEMINI_FEMALE_VOICES = [
    "Kore",
    "Aoede",
    "Leda",
    "Zephyr",
    "Callirrhoe",
    "Autonoe",
    "Despina",
    "Erinome",
    "Laomedeia",
    "Achernar",
    "Pulcherrima",
    "Vindemiatrix",
    "Sulafat",
]

GEMINI_MALE_VOICES = [
    "Puck",
    "Charon",
    "Fenrir",
    "Orus",
    "Enceladus",
    "Iapetus",
    "Umbriel",
    "Algieba",
    "Algenib",
    "Rasalgethi",
    "Alnilam",
    "Schedar",
    "Gacrux",
    "Achird",
    "Zubenelgenubi",
    "Sadachbia",
    "Sadaltager",
]

SUPPORTED_OUTPUT_LOCALES = [
    "fr-FR",
    "fr-CA",
    "es-ES",
    "es-US",
    "de-DE",
    "it-IT",
    "pt-BR",
    "pt-PT",
    "en-US",
    "en-GB",
    "nl-NL",
    "ru-RU",
    "ja-JP",
    "ko-KR",
    "zh-CN",
    "zh-TW",
    "ar-XA",
    "hi-IN",
    "pl-PL",
    "tr-TR",
    "sv-SE",
    "da-DK",
    "fi-FI",
    "no-NO",
    "el-GR",
    "he-IL",
    "id-ID",
    "th-TH",
    "uk-UA",
    "vi-VN",
    "cs-CZ",
    "ro-RO",
    "hu-HU",
]

MALE_TUTORS = [
    "Nicolas",
    "James",
    "Michael",
    "Mario",
    "Henry"
]

FEMALE_TUTORS = [
    "Renée",
    "Charlotte",
    "Sofia",
    "Kate",
    "Marie"
]

INPUT_LANGUAGES = [  # Supported languages by Gemini 3.5 Transcribe
    "Afrikaans",
    "Arabic",
    "Armenian",
    "Azerbaijani",
    "Belarusian",
    "Bosnian",
    "Bulgarian",
    "Catalan",
    "Chinese",
    "Croatian",
    "Czech",
    "Danish",
    "Dutch",
    "English",
    "Estonian",
    "Finnish",
    "French",
    "Galician",
    "German",
    "Greek",
    "Hebrew",
    "Hindi",
    "Hungarian",
    "Icelandic",
    "Indonesian",
    "Italian",
    "Japanese",
    "Kannada",
    "Kazakh",
    "Korean",
    "Latvian",
    "Lithuanian",
    "Macedonian",
    "Malay",
    "Marathi",
    "Maori",
    "Nepali",
    "Norwegian",
    "Persian",
    "Polish",
    "Portuguese",
    "Romanian",
    "Russian",
    "Serbian",
    "Slovak",
    "Slovenian",
    "Spanish",
    "Swahili",
    "Swedish",
    "Tagalog",
    "Tamil",
    "Thai",
    "Turkish",
    "Ukrainian",
    "Urdu",
    "Vietnamese",
    "Welsh"
]
