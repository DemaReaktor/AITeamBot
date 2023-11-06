import openai
import Config
from typing import Type
from validation import validate_text
from openai.error import RateLimitError, ServiceUnavailableError, OpenAIError


openai.api_key = Config.API_KEY


def send_request(system: str, content: str, model: str = "gpt-3.5-turbo") -> str:
    """send a request to the ChatGPT
    :param system is a description how the ChatGPT should answer
    :param content is a question which you want to set to the ChatGPT
    :param model is a model which will be used to set request to the ChatGPT, default is gpt-3.5-turbo
    :return an answer of the request"""
    validate_text(system)
    validate_text(content)
    completion = openai.ChatCompletion.create(model=model, messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": content},
        ])
    return completion.choices[0].message.content


def try_send_request(system: str, content: str, model: str = "gpt-3.5-turbo") -> str | Type[OpenAIError]:
    try:
        return send_request(system, content, model)
    except RateLimitError:
        return RateLimitError
    except ServiceUnavailableError:
        return ServiceUnavailableError
