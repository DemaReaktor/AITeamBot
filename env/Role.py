import OpenAIAPI
from validation import validate_text, validate_int
import inspect
import abc
import ast
from typing import Any
import json


def get_json(text: str) -> Any | None:
    return json.loads(ast.literal_eval(json.dumps(text)))


def validate_json(text: str) -> Any | None:
    try:
        # load json (ast.literal_eval(json.dumps()) need if properties have ' instead ")
        return json.loads(ast.literal_eval(json.dumps(text)))
    except():
        return None


def validate_syntax(text: str) -> bool:
    """check text is a Python code
    ignore ```"""
    validate_text(text)
    try:
        ast.parse(text.replace('```', ''))
        return True
    except SyntaxError:
        return False


class Role(abc.ABC):
    """send requests to ChatGPT using a system description"""

    def __init__(self, model: str = "gpt-3.5-turbo-16k"):
        self.__model = model

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, text):
        validate_text(text)
        self.__model = text

    def validate_answer(self, text: str) -> bool:
        """check ChatGPT answer is right as role need to answer"""
        return True

    def assistant(self) -> str | None:
        """an answer of ChatGpt which should be similar"""
        return None

    @abc.abstractmethod
    def system(self) -> str:
        """a description of how ChatGPT should answer the question"""
        pass

    def _change_text(self, text: str) -> str:
        """change text before it will be used for ChatGPT`s request"""
        return text

    def send_request(self, text: str) -> str | None:
        """send a request to the ChatGPT
        :param text is a question which you want to set to the ChatGPT
        :return an answer of the request if answer was validated otherwise None"""
        validate_text(text)
        result = OpenAIAPI.send_request(self.system(), self._change_text(text), self.assistant(), self.__model)
        if self.validate_answer(result):
            return result
        print(f"validation failed: {type(self)}, text:{result}")
        return None


class RoleWithTask(Role, abc.ABC):
    """Role which save id of task"""
    def __init__(self, task_id: int, *args, **kwargs):
        validate_int(task_id)
        self.__id = task_id
        super().__init__(*args, **kwargs)

    @property
    def task_id(self):
        """id of task role are created for"""
        return self.__id
