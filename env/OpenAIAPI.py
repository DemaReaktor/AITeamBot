import openai
import Config
from typing import Type
from validation import validate_text
from openai.error import RateLimitError, ServiceUnavailableError, OpenAIError


i = 0


def api_key():
    global i
    i += 1
    return Config.api_keys[i % len(Config.api_keys)]


openai.api_key = api_key()


def send_request(system: str, content: str, model: str = "gpt-3.5-turbo") -> str:
    """send a request to the ChatGPT
    :param system is a description how the ChatGPT should answer
    :param content is a question which you want to set to the ChatGPT
    :param model is a model which will be used to set request to the ChatGPT, default is gpt-3.5-turbo
    :return an answer of the request"""
    validate_text(system)
    validate_text(content)
    openai.api_key = Config.api_key()
    completion = openai.ChatCompletion.create(model=model, messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": content},
        ])
    print(completion)
    return completion.choices[0].message.content


def try_send_request(system: str, content: str, model: str = "gpt-3.5-turbo", max:int = 10) -> str | Type[OpenAIError]:
    try:
        return send_request(system, content, model)
    except RateLimitError:
        if max == 0:
            return RateLimitError
        return try_send_request(system, content, model, max - 1)
    except ServiceUnavailableError:
        return ServiceUnavailableError
