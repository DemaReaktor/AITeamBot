import openai
import Config
from validation import validate_text


openai.api_key = Config.API_KEY


def send_request(system: str, content: str, assistant: str | None = None, model: str = "gpt-3.5-turbo") -> str:
    """send a request to the ChatGPT
    :param system is a description how the ChatGPT should answer
    :param content is a question which you want to set to the ChatGPT
    :param model is a model which will be used to set request to the ChatGPT, default is gpt-3.5-turbo
    :param assistant what should be in the ChatGPT`s answer
    :return an answer of the request"""
    validate_text(system)
    validate_text(content)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": content},
        ]
    if not (assistant is None):
        messages.append({"role": "assistant", "content": assistant})
    completion = openai.ChatCompletion.create(model=model, messages=messages)
    return completion.choices[0].message.content
