from validation import validate_text
from mtranslate import translate as google_translate


def translate(text: str, from_language: str, to_language: str) -> str:
    """translate text
    :return translated text"""
    validate_text(text)
    validate_text(from_language)
    validate_text(to_language)
    return google_translate(text, from_language, to_language)
