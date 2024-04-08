from openai.error import OpenAIError
import OpenAIAPI
from validation import validate_text, validate_int
import abc
import ast
from typing import Any, Type
import json


def validate_bool(value: str):
    return value in ['так', 'ні']


def get_json(text: str) -> Any | None:
    return json.loads(ast.literal_eval(json.dumps(text)), strict=False)


def validate_json(text: str) -> Any | None:
    try:
        # load json (ast.literal_eval(json.dumps()) need if properties have ' instead ")
        return json.loads(ast.literal_eval(json.dumps(text)), strict=False)
    except json.JSONDecodeError:
        print("\njson no\n")
        return None


def validate_syntax(text: str) -> bool:
    """check text is a Python code
    ignore ```"""
    validate_text(text)
    try:
        ast.parse(text.replace('```', '').removeprefix('python'))
        return True
    except SyntaxError:
        return False


class Role(abc.ABC):
    """send requests to ChatGPT using a system description"""

    def __init__(self, model: str = "gpt-4"):
        self.model = model

    def validate_answer(self, text: str) -> bool:
        """check ChatGPT answer is right as role need to answer"""
        return True

    def example(self) -> list[str] | str | None:
        """an example of ChatGpt to write answer"""
        return None

    @abc.abstractmethod
    def system(self) -> str:
        """a description of how ChatGPT should answer the question"""
        pass

    def _change_text(self, text: str) -> str:
        """change text before it will be used for ChatGPT`s request"""
        return text

    def send_request(self, text: str) -> str | None | Type[OpenAIError]:
        """send a request to the ChatGPT
        :param text is a question which you want to set to the ChatGPT
        :return an answer of the request if answer was validated otherwise None"""
        validate_text(text)
        text_request = self.system()
        example = self.example()
        if not (example is None):
            if isinstance(example, str):
                text_request += " Приклад результату: " + example
            else:
                text_request += (" Приклад відповіді: " + ' .\nЩе приклад відповіді: '.join(example).
                                 removesuffix(' .\nЩе приклад відповіді: '))
        result = OpenAIAPI.try_send_request(text_request, self._change_text(text), self.__model)
        if not isinstance(result, str):
            return result
        if self.validate_answer(result):
            return result
        print(f"validation failed: {type(self)}, system:{text_request}, text:{result}")
        return None


class RoleWithTask(Role, abc.ABC):
    """Role which save data about task"""
    def __init__(self, task_id: int, chat_id: int, model: str = "gpt-4"):
        super().__init__(model)
        validate_int(task_id)
        validate_int(chat_id)
        self.task_id = task_id
        self.chat_id = chat_id
