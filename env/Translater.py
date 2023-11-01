from validation import validate_text


def translate(text: str, from_language: str, to_language: str) -> str:
    validate_text(text)
    validate_text(from_language)
    validate_text(to_language)
    return text
