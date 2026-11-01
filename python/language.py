from langcodes import Language, find
from google import genai
from typing import Optional
from python.consts import DEFAULT_FAST_MODEL

gemini_client: Optional[genai.Client] = None


def init_language(client: genai.Client) -> None:
    """
    Initialize Gemini client for translation and language detection

    :param client: a Google GenAI Client object
    """
    global gemini_client
    gemini_client = client


def translate(text: str, to: str) -> str:
    """
    Translate text using Gemini

    :param text: text to translate
    :param to: ISO 639-1 code of the language to translate the text to
    :return: translated text
    """
    target_lang_name = iso6391_to_language_name(to)
    interaction = gemini_client.interactions.create(
        model=DEFAULT_FAST_MODEL,
        system_instruction=(
            f"You are a professional translator. Translate the user's message into {target_lang_name} ({to}). "
            "Preserve any HTML formatting or line breaks if present. Output ONLY the translated text, "
            "with no explanations or surrounding quotes."
        ),
        input=text,
        store=False,
    )
    return (interaction.output_text or "").strip()


def detect_language(text: str) -> str:
    """
    Detect language of text using Gemini

    :param text: a string
    :return: ISO 639-1 code of the language detected (as string)
    """
    interaction = gemini_client.interactions.create(
        model=DEFAULT_FAST_MODEL,
        system_instruction=(
            "Identify the language of the user's text and respond with ONLY its 2-letter "
            "ISO 639-1 language code in lowercase (for example: fr, en, es, de, it). "
            "Output nothing else."
        ),
        input=text,
        store=False,
    )
    detected = (interaction.output_text or "").strip().lower()
    return detected.split()[0][:2] if detected else ""


def is_text_of_language(text: str, language_code: str) -> bool:
    """
    Whether or not the text is written in this language

    :param text: a string
    :param language_code: ISO 639-1 code of the language
    :return: True or False
    """
    return detect_language(text) == language_code.lower()


def language_name_to_iso6391(language_name: str) -> str:
    """
    Convert language name to ISO 639-1 code
    i.e.: English -> en

    :param language_name: string
    :return: ISO 639-1 code (as string)
    """
    return find(language_name).language


def iso6391_to_language_name(language_code: str, name_in_same_language: bool = False) -> str:
    """
    Convert ISO 639-1 code to language name

    :param language_code: ISO 639-1 code (as string)
    :param name_in_same_language: if True, name is returned in that language. Otherwise, name returns in English
                                  True: fr -> Français | False: fr -> French
    :return: language name
    """
    display_lang = language_code if name_in_same_language else "en"
    return Language.get(language_code).display_name(display_lang)


def locale_code_to_language(locale_code: str, name_in_same_language: bool = False):
    """
    Convert language code and locale (i.e. "fr-FR") to language name

    :param locale_code: string
    :param name_in_same_language: if True, name is returned in that language. Otherwise, name returns in English
                                  True: es-US -> Español (Estados Unidos) | False:es-US -> Spanish (United States)
    :return: language name
    """
    display_lang = locale_code.split('-')[0] if name_in_same_language else "en"
    return Language.get(locale_code).display_name(display_lang).title()
