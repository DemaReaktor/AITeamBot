from validation import validate_text


def translate(text: str, from_language: str, to_language: str) -> str:
    """translate text
    :return translated text"""
    validate_text(text)
    validate_text(from_language)
    validate_text(to_language)
    return text
